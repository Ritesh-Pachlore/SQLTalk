import google.generativeai as genai
from typing import Optional

def get_gemini_response(question: str, prompt: str) -> Optional[str]:
    """
    Get SQL query from Gemini based on natural language question
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')  # Using a faster model
        full_prompt = f"{prompt}\n\nQuestion: {question}\nSQL Query:"
        response = model.generate_content(full_prompt)
        
        # Clean the response
        sql_query = response.text.strip()
        # Remove any markdown formatting if present
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        return sql_query
    except Exception as e:
        print(f"Error generating SQL: {str(e)}")
        return None