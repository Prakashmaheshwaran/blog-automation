import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY_A = os.getenv("GOOGLE_API_KEY_A")
GOOGLE_API_KEY_B = os.getenv("GOOGLE_API_KEY_B")

def configure_genai(api_key):
    print(f"Configuring Generative AI with API")
    genai.configure(api_key=api_key)

def generate_text(prompt, i=1, max_output_tokens=2048):
    print(f"Entering generate_text")
    api_key = GOOGLE_API_KEY_A if i % 2 == 0 else GOOGLE_API_KEY_B
    print(f"Using API key: {'A' if i % 2 == 0 else 'B'}")
    configure_genai(api_key)
    
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": max_output_tokens,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    print("Creating GenerativeModel with specified configuration and safety settings.")
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    print("Starting a new chat.")
    convo = model.start_chat(history=[])
    
    print("Sending message to the model.")
    convo.send_message(prompt)
    
    print("Message sent, retrieving response.")
    return convo.last.text

def generate_blog(prompt, i=1):
    print(f"Entering generate_blog with prompt")
    api_key = GOOGLE_API_KEY_A if i % 2 == 0 else GOOGLE_API_KEY_B
    print(f"Using API key: {'A' if i % 2 == 0 else 'B'}")
    configure_genai(api_key)
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    print("Starting blog generation")
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text
