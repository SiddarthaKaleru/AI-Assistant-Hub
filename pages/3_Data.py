import streamlit as st
import pandas as pd
import google.generativeai as genai  # type: ignore
import io
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-pro')

st.set_page_config(page_title="Data Analysis Assistant")
st.title("AI-Powered Data Analysis Assistant")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("### Preview of Data", df.head())

        csv_string = df.to_csv(index=False)

        st.write("### Ask a question about your data:")
        query = st.text_input("")

        if st.button("Ask") and query:
            with st.spinner("Thinking..."):
                prompt = f"""You are a data analysis assistant. The user has uploaded a CSV file and asked a question. Here is the data (in CSV format): {csv_string} Now, answer the question based on the data: Question: {query}"""
                response = model.generate_content(prompt)
                st.write("### Answer:")
                st.write(response.text)

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to get started.")