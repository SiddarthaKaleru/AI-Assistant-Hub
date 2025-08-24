import streamlit as st
import pandas as pd
from groq import Groq
import os

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    st.error("Please ensure your GROQ_API_KEY is set in the .env file.")
    st.stop()

st.set_page_config(page_title="Data Analysis Assistant")
st.title("AI-Powered Data Analysis Assistant")
st.markdown("Upload a CSV and ask questions in plain English.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if 'df' not in st.session_state:
    st.session_state.df = None

if uploaded_file:
    try:
        st.session_state.df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.session_state.df = None

if st.session_state.df is not None:
    df = st.session_state.df
    st.success("File uploaded successfully!")
    
    with st.expander("Preview of Data"):
        st.dataframe(df.head())

    st.write("### Ask a question about your data:")
    query = st.text_input("e.g., 'What is the average value in the sales column?'", key="query_input")

    if st.button("Analyze", type="primary"):
        if query:
            with st.spinner("Analyzing..."):
                try:
                    csv_string = df.to_csv(index=False)
                    
                    system_prompt = "You are a data analysis expert. The user has provided a dataset in CSV format and a question. Your response should be clear, concise, and directly answer the question based on the data. If helpful, provide a brief summary or calculation."
                    user_content = f"Here is the data:\n```csv\n{csv_string}\n```\n\nHere is my question:\n{query}"
                    
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content},
                        ],
                        model="llama3-70b-8192",
                    )
                    response = chat_completion.choices[0].message.content
                    
                    st.markdown("### Analysis Result:")
                    st.markdown(response)

                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
        else:
            st.warning("Please enter a question to analyze.")
else:
    st.info("Please upload a CSV file to get started.")