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

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        
        # Get column names
        cur.execute(sql)
        columns = [description[0] for description in cur.description]
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        
        return {
            "columns": columns,
            "rows": rows,
            "success": True,
            "message": f"Successfully retrieved {len(rows)} records"
        }
    except sqlite3.Error as e:
        return {
            "success": False,
            "message": f"Database error: {str(e)}",
            "columns": [],
            "rows": []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"An error occurred: {str(e)}",
            "columns": [],
            "rows": []
        }

   
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

st.set_page_config(
    page_title="SQLTalk - Natural Language to SQL",
    page_icon="🗣️",
    layout="wide"
)

st.title("💬 SQLTalk")
st.subheader("Ask questions about your data in plain English")

# Add helpful instructions
st.markdown("""
### How to use SQLTalk:
1. Type your question in natural language
2. Click 'Ask the question' button
3. View the generated SQL and results

#### Available Data:
The database contains student information with these columns:
- NAME: Student's name
- CLASS: Course name (e.g., Data Science, DEVOPS)
- SECTION: Class section (A or B)
- MARKS: Student's marks

#### Example Questions:
- Show all students in Data Science class
- How many students scored above 80 marks?
- List students in section A
""")

# Initialize session state
if "input" not in st.session_state:
    st.session_state.input = ""

# Create a clean input section
st.markdown("### 🔍 Ask your question")
question = st.text_input(
    "Type your question in plain English",
    key="input",
    value=st.session_state.input,
    placeholder="e.g., Show all students in Data Science class"
)

# Add some spacing
st.markdown("")

# Create a centered button with custom styling
col1, col2, col3 = st.columns([1,1,1])
with col2:
    submit = st.button("🔎 Ask the question", use_container_width=True)

# if submit is clicked

if submit:
    with st.spinner('Generating SQL query...'):
        response = get_gemini_response(question, prompt)
        if response:
            # Show the generated SQL query
            st.subheader("Generated SQL Query:")
            st.code(response, language="sql")
            
            # Execute the query
            sql_response = read_sql_query(response, "student.db")
            
            if sql_response["success"]:
                st.success(sql_response["message"])
                
                # If we have data to display
                if sql_response["rows"]:
                    # Create a formatted table
                    st.subheader("Query Results:")
                    
                    # Convert the data to a format suitable for st.table
                    table_data = []
                    for row in sql_response["rows"]:
                        row_dict = {}
                        for col, val in zip(sql_response["columns"], row):
                            row_dict[col] = val
                        table_data.append(row_dict)
                    
                    # Display as an interactive table
                    st.dataframe(
                        table_data,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("Query executed successfully but returned no results.")
            else:
                st.error(sql_response["message"])









