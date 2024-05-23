import os
import csv
import random, requests, base64, textwrap
import time
import markdown
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from addons.image_fetcher import fetch_images_with_retries
from addons.genai_helper import generate_text, generate_blog
from addons.browser_automation import perform_steps
from addons.blog_link_retriver import get_published_and_scheduled_posts
from addons.image_helper import download_image, upload_image_to_wordpress, update_image_metadata, sanitize_filename

load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

AUTH_TOKEN = f"Basic {base64.b64encode(f'{WP_USERNAME}:{WP_PASSWORD}'.encode()).decode()}"
cta = """<br><br><a href="https://www.dynoxglobal.com">
<img src="https://dynoxglobal.com/wp-content/uploads/Dynox-global-call-to-action-medium-banner.gif" alt="Dynox Global Call to Action Banner" />
</a>"""
# Load prompts from a JSON file
def load_prompts(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

prompts = load_prompts('prompts.json')

def create_wordpress_post(title, content, image_id, future_time, category_id):
    future_time_iso = future_time.strftime('%Y-%m-%dT%H:%M:%S')

    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'title': title,
        'content': content,
        'status': 'future',
        'date': future_time_iso,
        'featured_media': image_id,
        'categories': [category_id]
    }
    response = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_wordpress_categories():
    headers = {'Authorization': AUTH_TOKEN}
    response = requests.get(f"{WP_URL}/wp-json/wp/v2/categories", headers=headers)
    response.raise_for_status()
    return response.json()

def generate_blog_structure(given_title):
    prompt = prompts['blog_structure_prompt'].format(title=given_title)
    return prompt

def generate_blog_tags(given_title, i):
    prompt = prompts['blog_tags_prompt'].format(given_title=given_title)
    tags = generate_text(prompt, i)
    tags = tags.replace("- ", "")
    tags = tags.replace("*", "")
    tags = tags.replace("\n", ",")
    return tags

def generate_single_word_for_topic(topic, i):
    prompt = prompts['single_word_prompt'].format(topic=topic)
    single_word = generate_text(prompt, i)
    return single_word.strip()

def generate_seo_title(title, i):
    prompt = prompts['seo_title_prompt'].format(title=title)
    seo_title = generate_text(prompt, i)
    seo_title = seo_title.strip()
    seo_title.replace("*", "")
    seo_title = textwrap.wrap(seo_title, width=59)
    return seo_title

def generate_meta_description(title, i):
    prompt = prompts['meta_description_prompt'].format(title=title)
    meta_description = generate_text(prompt, i)
    meta_description = meta_description.strip()
    meta_description.replace("*", "")
    meta_description = textwrap.wrap(meta_description, width=159)
    return meta_description

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            if len(row) < 2:
                continue  # Skip any rows that don't have at least two columns
            data.append((row[0].strip(), row[1].strip()))
    return data

csv_file_path = 'details.csv'
data = read_csv(csv_file_path)
num_images = 20
audience = "business owners, small business owners, entrepreneurs, founders"

future_time = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
future_time_str = future_time.strftime('%Y-%m-%d %H:%M:%S %Z')

print(f"Posting to domain: {WP_URL}")
print(f"Initial scheduled post time: {future_time_str}")

categories = get_wordpress_categories()
print("Available categories:")
for category in categories:
    print(f"{category['id']}: {category['name']}")

category_id = int(input("Enter the category ID to publish the blog post: "))
title_and_links = get_published_and_scheduled_posts()
input("Press Enter to confirm and proceed...")

for i, (keyword, given_title) in enumerate(data):
    try:
        image_search_term = generate_single_word_for_topic(keyword, i)
        image_urls = fetch_images_with_retries(keyword, num_images)
        selected_image_url = random.choice(image_urls)

        sanitized_title = sanitize_filename(given_title)
        download_path = f"{sanitized_title}.jpg"
        download_image(selected_image_url, download_path)

        image_id = upload_image_to_wordpress(download_path)
        update_image_metadata(image_id, given_title, i, prompts,keyword)

        structure = generate_blog_structure(given_title)

        blog_prompt = f"{prompts['full_blog_prompt'].format(given_title=given_title, titles_and_links=title_and_links, structure=structure, audience=audience)}"
        blog_content_md = generate_blog(blog_prompt, i)  # Generate the blog content using the new method
        blog_content_html = markdown.markdown(blog_content_md)  # Convert markdown to HTML

        tags = generate_blog_tags(given_title, i)

        content = f"{blog_content_html} + {cta}"

        seo_title = generate_seo_title(given_title, i)
        meta_description = generate_meta_description(given_title, i)

        minutes_offset = random.randint(15, 45)
        post_future_time = future_time + timedelta(hours=i*6)  # Increment by 6 hours for each post
        post_future_time = post_future_time.replace(minute=minutes_offset)

        post_response = create_wordpress_post(given_title, content, image_id, post_future_time, category_id)
        print("Post created with ID:", post_response['id'])
        print(f"View the scheduled post edit page at: {WP_URL}/wp-admin/post.php?post={post_response['id']}&action=edit")

        editable_link = f"{WP_URL}/wp-admin/post.php?post={post_response['id']}&action=edit"

        # Use the external script to open the site and input the necessary fields
        perform_steps(editable_link, tags + ",", keyword, seo_title, meta_description)

        Path(download_path).unlink()
        time.sleep(1.5)
    except Exception as e:
        print(f"An error occurred: {e}")
        continue
