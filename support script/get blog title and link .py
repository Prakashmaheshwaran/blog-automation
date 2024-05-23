import os
import csv
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

AUTH_TOKEN = f"Basic {base64.b64encode(f'{WP_USERNAME}:{WP_PASSWORD}'.encode()).decode()}"

def fetch_posts(status):
    headers = {
        'Authorization': AUTH_TOKEN
    }
    params = {
        'status': status,
        'per_page': 100  # Adjust as needed; maximum is 100 per request
    }
    response = requests.get(f"{WP_URL}/wp-json/wp/v2/posts", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def save_posts_to_csv(posts, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Slug Link'])
        for post in posts:
            title = post['title']['rendered']
            slug_link = f"{WP_URL.rstrip('/')}/{post['slug']}"
            writer.writerow([title, slug_link])

def main():
    try:
        published_posts = fetch_posts('publish')
        scheduled_posts = fetch_posts('future')
        all_posts = published_posts + scheduled_posts
        
        save_posts_to_csv(all_posts, 'published_and_scheduled_posts.csv')
        print("Published and scheduled posts saved to 'published_and_scheduled_posts.csv'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
