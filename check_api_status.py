from dotenv import load_dotenv
import os
import requests

load_dotenv()

def check_api_status():
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Test endpoint
    url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_api_status()