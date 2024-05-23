import os
import requests
from dotenv import load_dotenv
import base64

def fetch_posts(status, wp_url, auth_token):
    headers = {
        'Authorization': auth_token
    }
    params = {
        'status': status,
        'per_page': 100  # Adjust as needed; maximum is 100 per request
    }
    response = requests.get(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def format_posts(posts, wp_url):
    formatted_posts = ""
    for post in posts:
        title = post['title']['rendered']
        slug_link = f"{wp_url.rstrip('/')}/{post['slug']}"
        formatted_posts += f"{title} - {slug_link}, "
    return formatted_posts.rstrip(', ')

def get_published_and_scheduled_posts():
    load_dotenv()

    wp_url = os.getenv("WP_URL")
    wp_username = os.getenv("WP_USERNAME")
    wp_password = os.getenv("WP_PASSWORD")

    auth_token = f"Basic {base64.b64encode(f'{wp_username}:{wp_password}'.encode()).decode()}"

    try:
        published_posts = fetch_posts('publish', wp_url, auth_token)
        scheduled_posts = fetch_posts('future', wp_url, auth_token)
        all_posts = published_posts + scheduled_posts
        
        formatted_posts = format_posts(all_posts, wp_url)
        main_link = "Dynox Global home page - https://dynoxglobal.com/,Dynox global contact page - https://dynoxglobal.com/contact-us/,"
        return main_link+formatted_posts
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
# result = get_published_and_scheduled_posts()
# print(result)
