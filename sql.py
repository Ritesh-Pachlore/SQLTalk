from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3


import google.generativeai as genai

## Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # List available Gemini models
# for model in genai.list_models():
#     print(f"Model Name: {model.name}")
#     print(f"Display Name: {model.display_name}")
#     print(f"Description: {model.description}")
#     print("---")

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    import time
    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            model=genai.GenerativeModel('gemini-2.5-flash')  # Using a faster model
            response=model.generate_content(prompt + "\n" + question)
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

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()    
    for row in rows:
       print(row)
    return rows

   
## Define Your Prompt
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION

For example,
Example 1 - How many entries of records are present?,
the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;

Example 2 - Tell me all the students studying in Data Science class?,
the SQL command will be something like this SELECT * FROM STUDENT where CLASS="Data Science";
also the sql code should not have ``` in beginning or end and sql word in output
"""



## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

# Initialize session state
if "input" not in st.session_state:
    st.session_state.input = ""

question = st.text_input("Input: ", key="input", value=st.session_state.input)

submit=st.button("Ask the question")

# if submit is clicked

if submit:
    with st.spinner('Generating SQL query...'):
        response = get_gemini_response(question, prompt)
        if response:
            try:
                sql_response = read_sql_query(response, "student.db")
                st.subheader("The Response is")
                for row in sql_response:
                    print(row)
                    st.header(row)
            except Exception as e:
                st.error(f"Error executing SQL query: {str(e)}")
                st.code(response, language="sql")









