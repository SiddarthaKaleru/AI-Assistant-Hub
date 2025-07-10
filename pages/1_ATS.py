import base64
import io
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import pdf2image

load_dotenv()
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    st.error(f"Failed to configure Google API: {e}. Ensure your GOOGLE_API_KEY is set in the .env file.")
    st.stop()

PROMPTS = {
    "Fit Summary & Analysis": """
        You are a world-class resume evaluation expert and hiring manager for a top tech company.
        A candidate's multi-page resume and a job description are provided below.
        Your task is to conduct a comprehensive analysis and provide the following in clear, professional markdown:

        1.  **Overall Fit Summary:** A concise paragraph summarizing the candidate's suitability for the role.
        2.  **Estimated ATS Match Score:** A score from 0 to 100, representing the resume's alignment with the job description.
        3.  **Skill Match Analysis:**
            -   List the key required skills from the job description.
            -   Indicate with a ✔️ if the skill is clearly present in the resume, or ❌ if it is missing or not prominent.
        4.  **Experience Relevance:** Briefly analyze if the candidate’s work history and projects align with the role's responsibilities.
        5.  **Actionable Improvement Suggestions:** Provide specific, actionable advice on how the candidate can tailor their resume to better match this job (e.g., "Quantify achievement in Project X," "Add keywords like 'RESTful API' to your skills section").

        **If the job description is not provided:** Analyze the resume independently. Provide a summary of the candidate's key strengths and suggest 2-3 specific job titles or roles they are well-suited for.
    """,
    "Percentage Match": """
        You are an advanced Applicant Tracking System (ATS) simulator.
        Given the candidate's resume and a job description, your task is to calculate a precise match percentage.
        Provide only the following:
        1.  **Match Percentage (0–100%):** Based on a deep analysis of keyword overlap, required skills, years of experience, and educational qualifications.
        2.  **Rationale:** In 3-4 bullet points, explain the key factors that influenced the score (both positive and negative).

        **If the job description is not provided:** Analyze the resume's general strength. Estimate a "General ATS-Friendliness" score and suggest 2-3 job roles it's optimized for.
    """,
    "Resume Parser": """
        You are a highly accurate, machine-learning-powered resume parser.
        Your task is to extract structured information from the provided resume pages. Present the output in clean, well-organized markdown format.
        Extract the following sections if present:
        -   **Contact Information:** (Name, Email, Phone, LinkedIn, GitHub)
        -   **Professional Summary/Objective**
        -   **Work Experience:** (For each job: Job Title, Company, Location, Dates, Key Responsibilities/Achievements as bullet points)
        -   **Education:** (Degree, Major, University, Dates, GPA/Score)
        -   **Technical Skills:** (Categorize into Languages, Frameworks, Tools, etc., if possible)
        -   **Projects:** (Project Title, Tech Stack, Key Features/Contributions as bullet points)
        -   **Certifications & Awards**
    """,
    "Red Flags Checker": """
        You are an expert resume auditor for a top recruitment agency.
        Scrutinize the provided resume pages for any potential red flags or issues that might cause a recruiter to discard it.
        Check for and list any of the following problems:
        -   **ATS Formatting Issues:** (e.g., use of columns, tables, images, headers/footers, non-standard fonts that can confuse parsers).
        -   **Vague or Overused Language:** (e.g., "team player," "results-oriented" without concrete evidence).
        -   **Missing Quantifiable Results:** (e.g., lack of numbers, percentages, or specific outcomes in project/work descriptions).
        -   **Spelling and Grammatical Errors.**
        -   **Inconsistent Formatting:** (e.g., different date formats, inconsistent use of bolding).
        -   **Unprofessional Details:** (e.g., unprofessional email address, irrelevant personal information).
    """
}


def get_gemini_response(prompt, pdf_parts, job_description=""):
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        content_to_send = [prompt]
        if job_description:
            content_to_send.append(job_description)
        
        content_to_send.extend(pdf_parts)
        
        response = model.generate_content(content_to_send)
        return response.text
    except Exception as e:
        return f"An error occurred while calling the Gemini API: {e}"

def process_and_store_pdf(uploaded_file):
    if uploaded_file is None:
        st.session_state.pdf_content = None
        return

    try:
        if 'processed_file_name' not in st.session_state or st.session_state.processed_file_name != uploaded_file.name:
            with st.spinner("Processing PDF... This may take a moment for multi-page documents."):
                images = pdf2image.convert_from_bytes(uploaded_file.read())
                
                pdf_parts = []
                for image in images:
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='JPEG')
                    img_byte_arr = img_byte_arr.getvalue()

                    pdf_parts.append({
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte_arr).decode()
                    })
                
                st.session_state.pdf_content = pdf_parts
                st.session_state.processed_file_name = uploaded_file.name
                st.success(f"Successfully processed {len(images)}-page resume: '{uploaded_file.name}'")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        st.session_state.pdf_content = None


st.set_page_config(page_title="ATS Resume Expert", layout="wide", initial_sidebar_state="auto")
st.title(" ATS Resume Analyzer")
st.markdown("Get instant, AI-powered feedback on your resume.")

if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = None
if 'processed_file_name' not in st.session_state:
    st.session_state.processed_file_name = None

col1, col2 = st.columns([0.4, 0.6])

with col1:
    st.subheader("1. Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)...",
        type=["pdf"],
        help="The entire document will be analyzed."
    )
    if uploaded_file:
        process_and_store_pdf(uploaded_file)

with col2:
    st.subheader("2. Paste Job Description (Optional)")
    job_description = st.text_area(
        "For the best results, provide the full job description here.",
        height=250,
        key="job_desc"
    )

st.divider()

st.subheader("3. Choose Analysis Type & Run")
analysis_type = st.radio(
    "Select an analysis to perform:",
    options=list(PROMPTS.keys()),
    horizontal=True,
    label_visibility="collapsed"
)

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if st.session_state.pdf_content:
        with st.spinner(f" Running '{analysis_type}' analysis..."):
            prompt_to_use = PROMPTS[analysis_type]   
            response = get_gemini_response(prompt_to_use, st.session_state.pdf_content, job_description)
            st.markdown(f"--- \n ### Results for: {analysis_type}")
            st.markdown(response)
    else:
        st.error("Please upload a PDF resume first.")