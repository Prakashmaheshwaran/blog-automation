import requests

def get_user_details(access_token):
    url = 'https://api.medium.com/v1/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # If the request was successful, parse the JSON response
        user_data = response.json().get('data')
        return user_data
    else:
        # If the request failed, print the status code and response text
        print(f"Failed to retrieve user details. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Configuration variable
ACCESS_TOKEN = '260eec10aea8bc50e934cfe12325234acd0b980b2cca269310ed2224a2b51830b'  # Replace with your actual access token

# Get user details
user_details = get_user_details(ACCESS_TOKEN)
if user_details:
    print(f"User ID: {user_details['id']}")
    print(f"Username: {user_details['username']}")
    print(f"Name: {user_details['name']}")
    print(f"Profile URL: {user_details['url']}")
else:
    print("Failed to retrieve user details.")
