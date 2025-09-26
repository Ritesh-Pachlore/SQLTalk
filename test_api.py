from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

def test_api():
    try:
        # Configure the API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Create a simple model instance
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Make a simple test query
        response = model.generate_content("Say 'API is working!' if you can read this.")
        
        print("API Test Result:", response.text)
        print("API Key is working correctly!")
        return True
        
    except Exception as e:
        print("Error testing API:", str(e))
        return False

if __name__ == "__main__":
    test_api()