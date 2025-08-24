import streamlit as st
from groq import Groq
import os

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    st.error("Please ensure your GROQ_API_KEY is set in the .env file.")
    st.stop()
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Conversational AI Chatbot")
st.title("AI Conversational Chatbot")
st.markdown("Powered by Groq and Llama 3")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("What's on your mind?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.chat_history,
                model="llama3-70b-8192",
            )
            bot_reply = chat_completion.choices[0].message.content
            
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(bot_reply)

        except Exception as e:
            st.error(f"An error occurred: {e}")