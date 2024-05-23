import requests

def create_post(access_token, user_id, title, image_url, link_url):
    url = f'https://api.medium.com/v1/users/{user_id}/posts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'User-Agent': 'Mozilla/5.0 (compatible; YourBotName/1.0)'  # Customize appropriately
    }
    json_data = {
        'title': title,
        'contentFormat': 'html',
        'content': f'<img src="{image_url}" alt="Linked Image"/> hello the world is in danger',
        'publishStatus': 'draft'
    }
    response = requests.post(url, headers=headers, json=json_data)

    try:
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return response.json()  # Assuming the successful response is always JSON
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        print(f"Response Content: {response.text}")

    return None  # If an error occurs or the response can't be decoded, return None

# Example usage
ACCESS_TOKEN = '260eec10aea8bc50e934cfe12325234acd0b980b2cca269310ed2224a2b51830b'
USER_ID = '1410428f1dea8c458d917d442157e803084c84aef7aba98a52e99e8eb385a1ed3'
POST_TITLE = 'Your Post Title'
IMAGE_URL = 'https://dynoxglobal.com/wp-content/uploads/project-thumb-3-style2-1.png'
LINK_URL = 'https://google.com'

post_response = create_post(ACCESS_TOKEN, USER_ID, POST_TITLE, IMAGE_URL, LINK_URL)
if post_response:
    print("Post created successfully:", post_response)
else:
    print("Failed to create post.")
