import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def fetch_pexels_landscape_images(keyword, num_images=20):
    print("Entering fetch_pexels_landscape_images")
    pexels_search_url = 'https://api.pexels.com/v1/search'
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    params = {
        'query': keyword,
        'per_page': num_images,
        'orientation': 'landscape'
    }
    response = requests.get(pexels_search_url, headers=headers, params=params)
    print(f"Response status code for Pexels: {response.status_code}")
    if response.status_code == 200:
        image_data_list = response.json()['photos']
        print("Fetched images from Pexels successfully")
        return [image_data['src']['large'] for image_data in image_data_list]
    else:
        print(f"Failed to fetch images from Pexels. Status code: {response.status_code}")
        raise Exception(f"Failed to fetch images. Status code: {response.status_code}, Message: {response.json()}")

def fetch_pixabay_landscape_images(keyword, num_images=20):
    print("Entering fetch_pixabay_landscape_images")
    pixabay_search_url = 'https://pixabay.com/api/'
    params = {
        'key': PIXABAY_API_KEY,
        'q': keyword,
        'image_type': 'photo',
        'orientation': 'horizontal',
        'per_page': num_images
    }
    response = requests.get(pixabay_search_url, params=params)
    print(f"Response status code for Pixabay: {response.status_code}")
    if response.status_code == 200:
        image_data_list = response.json()['hits']
        print("Fetched images from Pixabay successfully")
        return [image_data['largeImageURL'] for image_data in image_data_list]
    else:
        print(f"Failed to fetch images from Pixabay. Status code: {response.status_code}")
        raise Exception(f"Failed to fetch images. Status code: {response.status_code}, Message: {response.json()}")

def fetch_unsplash_landscape_images(keyword, num_images=20):
    print("Entering fetch_unsplash_landscape_images")
    unsplash_search_url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': keyword,
        'per_page': num_images,
        'orientation': 'landscape',
        'client_id': UNSPLASH_ACCESS_KEY
    }
    response = requests.get(unsplash_search_url, params=params)
    print(f"Response status code for Unsplash: {response.status_code}")
    if response.status_code == 200:
        image_data_list = response.json()['results']
        print("Fetched images from Unsplash successfully")
        return [image_data['urls']['regular'] for image_data in image_data_list]
    else:
        print(f"Failed to fetch images from Unsplash. Status code: {response.status_code}")
        raise Exception(f"Failed to fetch images. Status code: {response.status_code}, Message: {response.json()}")

def fetch_images_with_retries(keyword, num_images=10):
    print("Entering fetch_images_with_retries")
    fetch_functions = [
        lambda: fetch_unsplash_landscape_images(keyword, num_images),
        lambda: fetch_pixabay_landscape_images(keyword, num_images),
        lambda: fetch_pexels_landscape_images(keyword, num_images)
    ]
    for attempt in range(3):  # Try 3 times in total
        fetch_function = random.choice(fetch_functions)
        print(f"Attempt {attempt + 1}: Fetching images from {fetch_function.__name__}")
        try:
            images = fetch_function()
            print("Images fetched successfully")
            return images
        except Exception as e:
            print(f"Error fetching images: {e}")
            continue
    
    # Return dummy URLs if no images are fetched after retries
    print("Failed to fetch images after 3 attempts, returning dummy images")
    return [
        "https://dynoxglobal.com/wp-content/uploads/project-thumb-6-style2-1.png",
        "https://dynoxglobal.com/wp-content/uploads/project-thumb-5-style2-1.png",
        "https://dynoxglobal.com/wp-content/uploads/project-thumb-4-style2-1.png",
        "https://dynoxglobal.com/wp-content/uploads/project-thumb-7-style2-1.png"
    ]
