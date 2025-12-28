# Create a Streamlit web application that allows users to connect to a MySQL database and ask natural language questions. The app should generate and execute SELECT SQL queries using an LLM and display both the query results and a simple English explanation.
# Use the sample MySQL connection parameters provided in connection.txt and the sample database schema in db.txt for testing.
# pip install mysql-connector-python
import streamlit as st
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
st.set_page_config(page_title="NL to SQL - MySQL", layout="wide")
st.title("🤖 Natural Language to SQL Query")

# MySQL Connection Details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "manager",  
    "database": "company"         
}
# Connect to MySQL
@st.cache_resource
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

try:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    st.success("✅ Connected to MySQL Database")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# Database Schema (from db.txt)
SCHEMA = """
    Table: employees
    Columns:
    - id (INT)
    - name (VARCHAR)
    - department (VARCHAR)
    - salary (INT)
    - joining_date (DATE)
"""
# Initialize LLM
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# User Input
question = st.text_input("❓ Ask a question about the database")

if st.button("Generate & Execute SQL"):
    if not question.strip():
        st.warning("Please enter a question")
        st.stop()
    # Prompt: Natural Language → SQL
    sql_prompt = f"""
    You are an expert MySQL developer.

    Database schema:
    {SCHEMA}

    User question:
    {question}

    Rules:
    - Generate ONLY a SELECT SQL query
    - Do NOT use INSERT, UPDATE, DELETE
    - No explanation
    - No markdown
    """

    try:
        sql_query = llm.invoke(sql_prompt).content.strip()

        st.subheader("🧾 Generated SQL Query")
        st.code(sql_query, language="sql")

        # Safety check
        if not sql_query.lower().startswith("select"):
            st.error("Only SELECT queries are allowed.")
            st.stop()
        # Execute SQL Query
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        if not rows:
            st.warning("No results found.")
            st.stop()

        df = pd.DataFrame(rows)

        st.subheader("📊 Query Results")
        st.dataframe(df)
        # Explain result in simple English
        explain_prompt = f"""
            The following is the result of a SQL query:

            {df.to_string(index=False)}

            Explain this result in simple English for a non-technical user.
        """

        explanation = llm.invoke(explain_prompt).content

        st.subheader("🗣️ Explanation")
        st.write(explanation)

    except Exception as e:
        st.error(f"Error: {e}")
