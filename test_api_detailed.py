from dotenv import load_dotenv
import os
import google.generativeai as genai
import time

load_dotenv()

def test_api_with_details():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"Testing API key: {api_key[:6]}...{api_key[-4:]}")  # Show only part of the key for security
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List available models (this helps verify API access)
        print("\nChecking available models...")
        models = genai.list_models()
        for model in models:
            print(f"Found model: {model.name}")
        
        # Try a simple generation
        print("\nTesting content generation...")
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Return only the number 1 if you can read this.")
        
        print("Response from API:", response.text)
        print("\nAPI Test Status: SUCCESS")
        return True
        
    except Exception as e:
        print("\nAPI Test Status: FAILED")
        print("Error details:", str(e))
        
        if "429" in str(e):
            print("\nThis is a rate limit error. Possible causes:")
            print("1. The API key is too new (wait 5-10 minutes)")
            print("2. The project needs billing enabled")
            print("3. Multiple requests were made too quickly")
            print("\nRecommended actions:")
            print("- Wait a few minutes and try again")
            print("- Visit https://makersuite.google.com/app/apikey to check key status")
            print("- Enable billing at https://console.cloud.google.com/billing")
        return False

if __name__ == "__main__":
    print("Starting API test...")
    test_api_with_details()