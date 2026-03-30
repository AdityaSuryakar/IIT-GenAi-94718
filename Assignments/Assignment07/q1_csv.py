# # Q1:
# Create a Streamlit application that allows users to upload a CSV file and view its schema.
# Use an LLM to convert user questions into SQL queries, execute them on the CSV data using pandasql, 
# and explain the results in simple English.

import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("📊 CSV Query Assistant (SQL + LLM)")

with st.sidebar:
    st.title("🗃️ File Uploader")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        st.write("File uploaded successfully!")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 CSV Preview")
    st.dataframe(df.head())
    st.subheader("🧩 CSV Schema")
    schema_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })
    st.table(schema_df)

    question = st.text_input("❓ Ask a question about this CSV")

    if st.button("Generate & Run SQL"):
        if not question:
            st.warning("Please enter a question")
        else:
            llm_prompt = f"""
            You are an expert SQL developer.

            Table name: data

            Table schema:
            {schema_df.to_string(index=False)}

            User question:
            {question}

            Instruction:
            Generate ONLY a valid SQLite SQL query.
            Do NOT add explanation.
            Do NOT add markdown.
            If not possible, return Error.
            """

            try:
                sql_query = llm.invoke(llm_prompt).content.strip()

                st.subheader("🧾 Generated SQL Query")
                st.code(sql_query, language="sql")

                if sql_query.lower() == "error":
                    st.error("LLM could not generate SQL for this question.")
                else:
                    result_df = sqldf(sql_query, {"data": df})

                    st.subheader("📈 Query Result")
                    st.dataframe(result_df)
                    explain_prompt = f"""
                    The following is the result of a SQL query:
                    {result_df.to_string(index=False)}

                    Explain this result in simple English for a non-technical user.
                    """

                    explanation = llm.invoke(explain_prompt).content

                    st.subheader("🤖 Explanation")
                    st.write(explanation)

            except Exception as e:
                st.error(f"Error executing query: {e}")
