import streamlit as st

st.set_page_config(page_title="AI Assistant Hub", layout="wide")

st.title("Welcome to the AI Assistant Hub")
st.markdown("""
This is a one-stop portal for powerful AI tools designed to streamline your tasks.
Whether you're polishing your resume, analyzing data, or just looking for a smart conversational partner, you'll find a helpful assistant here.
""")
st.markdown("### Choose a tool to get started:")

st.divider()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("ATS Resume Expert")
        st.write("Upload your resume and a job description to get an in-depth analysis, match score, and improvement tips.")
        if st.button("Launch ATS Expert", key="ats", use_container_width=True):
            st.switch_page("pages/1_ATS.py")

with col2:
    with st.container(border=True):
        st.subheader("AI Conversational ChatBot")
        st.write("Chat with an advanced AI that can answer questions, write content, and assist with a variety of tasks.")
        if st.button("Start Chatting", key="chat", use_container_width=True):
            st.switch_page("pages/2_ChatBot.py")

with col3:
    with st.container(border=True):
        st.subheader("Data Analysis Assistant")
        st.write("Upload a CSV and ask questions in plain English to get insights, summaries, and data analysis.")
        if st.button("Analyze Data", key="data", use_container_width=True):
            st.switch_page("pages/3_Data.py")