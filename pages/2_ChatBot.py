import streamlit as st
import google.generativeai as genai 
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-pro')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Conversational AI Chatbot")
st.title("AI Conversational Chatbot")

user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    with st.spinner("Thinking..."):
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        gemini_messages = [
            {"role": msg["role"], "parts": [msg["text"]]} for msg in st.session_state.chat_history
        ]
        response = model.generate_content(gemini_messages)
        bot_reply = response.text
        st.session_state.chat_history.append({"role": "model", "text": bot_reply})

st.markdown("### Conversation")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")

