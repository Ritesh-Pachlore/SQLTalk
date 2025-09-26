import time
import streamlit as st
import google.generativeai as genai

def get_gemini_response(question, prompt):
    """
    Get response from Gemini API with retry mechanism.
    
    Args:
        question (str): The user's question
        prompt (str): The system prompt/context
    
    Returns:
        str: Generated SQL query or None if failed
    """
    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')  # Using a faster model
            response = model.generate_content(prompt + "\n" + question)
            return response.text
        except Exception as e:
            if "429" in str(e) and retry_count < max_retries - 1:  # Rate limit error
                retry_count += 1
                wait_time = 5  # Start with a 5 second wait
                st.warning(f"Rate limit reached. Waiting {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                st.error(f"An error occurred: {str(e)}")
                return None
    return None