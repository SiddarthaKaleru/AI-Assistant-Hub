import streamlit as st

st.set_page_config(page_title="Home", layout="centered")

st.title("Welcome to the AI Assistant Hub")
st.markdown("### Choose a tool to get started:")

st.markdown("")

col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])

with col2:
    if st.button("ATS Resume Expert"):
        st.switch_page("pages/1_ATS.py")

with col3:
    if st.button("AI Conversational ChatBot"):
        st.switch_page("pages/2_ChatBot.py")

with col4:
    if st.button("Data Analysis Assistant"):
        st.switch_page("pages/3_Data.py")