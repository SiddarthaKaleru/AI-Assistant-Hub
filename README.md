**AI Assistant Hub (Streamlit + Gemini Pro)**
The AI Assistant Hub is a multi-functional Streamlit web application powered by Google's Gemini 2.5 Pro LLM. It offers intelligent tools to assist users with resume analysis, chatbot interaction, and data analysis, all from a single unified interface.

Features
ATS Resume Expert
Upload a PDF resume and (optionally) a job description. Get:

ATS match score and skill comparison
Resume parsing into structured sections
Red flag detection and formatting tips
Tailored improvement suggestions using Gemini LLM prompts

AI Conversational ChatBot
An interactive, memory-aware chatbot that responds contextually to your queries using Gemini 2.5. Chat history is retained in session for a seamless conversation.

Data Analysis Assistant
Upload a CSV file and ask natural language questions about your data. The assistant reads, understands, and generates insights using the underlying LLM.

🛠Tech Stack
Frontend: Streamlit
AI Engine: Google Gemini 2.5 Pro via google.generativeai
PDF Handling: pdf2image, Pillow
Environment Management: python-dotenv
