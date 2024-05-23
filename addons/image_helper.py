import os
import requests
import re,base64
from dotenv import load_dotenv
from addons.genai_helper import generate_text

load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

AUTH_TOKEN = f"Basic {base64.b64encode(f'{WP_USERNAME}:{WP_PASSWORD}'.encode()).decode()}"

def sanitize_filename(filename):
    # Remove any character that is not a letter, number, hyphen, or underscore
    return re.sub(r'[^a-zA-Z0-9-_]', '', filename)

def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def upload_image_to_wordpress(image_path):
    files = {'file': open(image_path, 'rb')}
    headers = {'Authorization': AUTH_TOKEN}
    response = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, files=files)
    response.raise_for_status()
    print("Image uploaded with ID:", response.json()['id'])
    return response.json()['id']

def update_image_metadata(image_id, title, i, prompts,keyword):
    alt_text_prompt = prompts['alt_text_prompt'].format(title=title)
    caption_prompt = prompts['caption_prompt'].format(title=title)
    description_prompt = prompts['description_prompt'].format(title=title)

    alt_text = generate_text(alt_text_prompt, i)
    caption = generate_text(caption_prompt, i)
    description = generate_text(description_prompt, i)
    attach = " - " + keyword + " - Dynox Global"

    media_details = {
        'title': title + attach,
        'description': description + attach,
        'caption': caption + attach,
        'alt_text': alt_text + attach
    }
    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{WP_URL}/wp-json/wp/v2/media/{image_id}", headers=headers, json=media_details)
    response.raise_for_status()
    print("Media metadata updated for ID:", image_id)
