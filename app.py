from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from src.database import read_sql_query
from src.gemini_handler import get_gemini_response

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt template
PROMPT_TEMPLATE = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION

For example,
Example 1 - How many entries of records are present?,
the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;

Example 2 - Tell me all the students studying in Data Science class?,
the SQL command will be something like this SELECT * FROM STUDENT where CLASS="Data Science";
also the sql code should not have ``` in beginning or end and sql word in output
"""

def main():
    # Configure Streamlit page
    st.set_page_config(page_title="SQL Talk - Natural Language to SQL")
    st.header("SQL Talk: Natural Language to SQL Query")
    st.caption("Ask questions about your database in plain English")

    # Initialize session state
    if "input" not in st.session_state:
        st.session_state.input = ""

    # Create the input form
    question = st.text_input("Your Question:", key="input", 
                           value=st.session_state.input,
                           placeholder="e.g., Show all students in Data Science class")

    submit = st.button("Get Answer")

    # Process the question when submitted
    if submit:
        with st.spinner('Generating SQL query...'):
            response = get_gemini_response(question, PROMPT_TEMPLATE)
            if response:
                try:
                    st.code(response, language="sql")
                    sql_response = read_sql_query(response, "data/student.db")
                    st.subheader("Results:")
                    for row in sql_response:
                        st.write(row)
                except Exception as e:
                    st.error(f"Error executing SQL query: {str(e)}")
                    st.code(response, language="sql")

if __name__ == "__main__":
    main()