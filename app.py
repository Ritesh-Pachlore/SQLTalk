from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from src.database import read_sql_query, get_query_results_with_columns, validate_sql_query
from src.gemini_handler import get_gemini_response
from src.schema_analyzer import get_database_schema, format_schema_for_prompt
from src.prompt_builder import build_dynamic_prompt
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def main():
    # Configure Streamlit page
    st.set_page_config(page_title="SQL Talk - Natural Language to SQL", layout="wide")
    st.header("SQL Talk: Natural Language to SQL Query")
    st.caption("Ask questions about your database in plain English")
    
    # Sidebar for database configuration
    with st.sidebar:
        st.header("Database Configuration")
        
        # Database selection
        db_type = st.selectbox("Database Type", ["SQLite", "MySQL", "PostgreSQL"])
        
        # For now, we'll use SQLite
        if db_type == "SQLite":
            db_path = st.text_input("Database Path", value="data/student.db")
            
            if st.button("Analyze Database Schema"):
                try:
                    schema = get_database_schema(db_path)
                    st.session_state.schema = schema
                    st.session_state.schema_text = format_schema_for_prompt(schema)
                    st.success("Schema analyzed successfully!")
                except Exception as e:
                    st.error(f"Error analyzing schema: {str(e)}")
        
        # Display schema if available
        if "schema" in st.session_state:
            st.subheader("Database Schema")
            for table, columns in st.session_state.schema.items():
                with st.expander(f"Table: {table}"):
                    for col_name, col_type in columns:
                        st.text(f"{col_name} ({col_type})")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Ask Your Question")
        
        # Example questions
        if "schema" in st.session_state:
            st.info("Example questions:")
            examples = [
                "Show all records",
                "Count total number of entries",
                "Find all students in Data Science class",
                "Show students with marks greater than 80",
                "What is the average marks?",
                "List all unique classes"
            ]
            for example in examples:
                if st.button(example, key=f"example_{example}"):
                    st.session_state.input = example
        
        # Question input
        question = st.text_area("Your Question:", 
                               value=st.session_state.get("input", ""),
                               placeholder="e.g., Show all students in Data Science class",
                               height=100)
        
        submit = st.button("Generate SQL & Execute", type="primary")
    
    with col2:
        if submit and question:
            if "schema_text" not in st.session_state:
                st.error("Please analyze the database schema first (use sidebar)")
            else:
                with st.spinner('Generating SQL query...'):
                    # Build dynamic prompt
                    prompt = build_dynamic_prompt(st.session_state.schema_text)
                    
                    # Get SQL from Gemini
                    sql_query = get_gemini_response(question, prompt)
                    
                    if sql_query:
                        st.subheader("Generated SQL Query")
                        st.code(sql_query, language="sql")
                        
                        # Validate SQL
                        if not validate_sql_query(sql_query):
                            st.error("Generated query contains potentially dangerous operations or is not a SELECT query")
                        else:
                            try:
                                # Execute query
                                columns, results = get_query_results_with_columns(sql_query, db_path)
                                
                                st.subheader("Query Results")
                                if results:
                                    # Display as dataframe
                                    df = pd.DataFrame(results, columns=columns)
                                    st.dataframe(df, use_container_width=True)
                                    
                                    # Show summary
                                    st.caption(f"Returned {len(results)} row(s)")
                                    
                                    # Download option
                                    csv = df.to_csv(index=False)
                                    st.download_button(
                                        label="Download as CSV",
                                        data=csv,
                                        file_name="query_results.csv",
                                        mime="text/csv"
                                    )
                                else:
                                    st.info("Query executed successfully but returned no results")
                                    
                            except Exception as e:
                                st.error(f"Error executing SQL query: {str(e)}")
                    else:
                        st.error("Failed to generate SQL query")

if __name__ == "__main__":
    main()