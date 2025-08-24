import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import fitz 

load_dotenv()

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Failed to configure Groq API: {e}. Ensure your GROQ_API_KEY is set in the .env file.")
    st.stop()

PROMPTS = {
    "Fit Summary & Analysis": """
        You are a world-class resume evaluation expert and hiring manager for a top tech company.
        The extracted text from a candidate's resume and a job description are provided below.
        Your task is to conduct a comprehensive analysis and provide the following in clear, professional markdown:

        1.  **Overall Fit Summary:** A concise paragraph summarizing the candidate's suitability for the role.
        2.  **Estimated ATS Match Score:** A score from 0 to 100, representing the resume's alignment with the job description.
        3.  **Skill Match Analysis:**
            -   List the key required skills from the job description.
            -   Indicate with a ✔️ if the skill is clearly present in the resume, or ❌ if it is missing or not prominent.
        4.  **Experience Relevance:** Briefly analyze if the candidate’s work history and projects align with the role's responsibilities.
        5.  **Actionable Improvement Suggestions:** Provide specific, actionable advice on how the candidate can tailor their resume to better match this job (e.g., "Quantify achievement in Project X," "Add keywords like 'RESTful API' to your skills section").

        **If the job description is not provided:** Analyze the resume text independently. Provide a summary of the candidate's key strengths and suggest 2-3 specific job titles or roles they are well-suited for.
    """,
    "Percentage Match": """
        You are an advanced Applicant Tracking System (ATS) simulator.
        Given the candidate's resume text and a job description, your task is to calculate a precise match percentage.
        Provide only the following:
        1.  **Match Percentage (0–100%):** Based on a deep analysis of keyword overlap, required skills, years of experience, and educational qualifications.
        2.  **Rationale:** In 3-4 bullet points, explain the key factors that influenced the score (both positive and negative).

        **If the job description is not provided:** Analyze the resume's general strength. Estimate a "General ATS-Friendliness" score and suggest 2-3 job roles it's optimized for.
    """,
    "Resume Parser": """
        You are a highly accurate, machine-learning-powered resume parser.
        Your task is to extract structured information from the provided resume text. Present the output in clean, well-organized markdown format.
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
        Scrutinize the provided resume text for any potential red flags or issues that might cause a recruiter to discard it.
        Check for and list any of the following problems:
        -   **Vague or Overused Language:** (e.g., "team player," "results-oriented" without concrete evidence).
        -   **Missing Quantifiable Results:** (e.g., lack of numbers, percentages, or specific outcomes in project/work descriptions).
        -   **Spelling and Grammatical Errors.**
        -   **Inconsistent Formatting:** (e.g., different date formats, inconsistent use of bolding).
        -   **Unprofessional Details:** (e.g., unprofessional email address, irrelevant personal information).
    """
}

def get_groq_response(system_prompt, user_content):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while calling the Groq API: {e}"

def process_and_store_pdf(uploaded_file):
    if uploaded_file is None:
        st.session_state.pdf_text_content = None
        return

    try:
        if 'processed_file_name' not in st.session_state or st.session_state.processed_file_name != uploaded_file.name:
            with st.spinner("Extracting text from PDF..."):
                pdf_bytes = uploaded_file.read()
                # Open the PDF from bytes
                pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                
                # Extract text from all pages
                full_text = ""
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    full_text += page.get_text()
                
                st.session_state.pdf_text_content = full_text
                st.session_state.processed_file_name = uploaded_file.name
                st.success(f"Successfully processed resume: '{uploaded_file.name}'")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        st.session_state.pdf_text_content = None

st.set_page_config(page_title="ATS Resume Expert", layout="wide", initial_sidebar_state="auto")
st.title("ATS Resume Analyzer")
st.markdown("Get instant, AI-powered feedback on your resume.")

if 'pdf_text_content' not in st.session_state:
    st.session_state.pdf_text_content = None
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
    if st.session_state.pdf_text_content:
        with st.spinner(f"Running '{analysis_type}' analysis..."):
            system_prompt = PROMPTS[analysis_type]
            
            # Combine resume text and job description for the user content
            user_content = f"RESUME TEXT:\n{st.session_state.pdf_text_content}\n\n"
            if job_description:
                user_content += f"JOB DESCRIPTION:\n{job_description}"
                
            response = get_groq_response(system_prompt, user_content)
            st.markdown(f"--- \n ### Results for: {analysis_type}")
            st.markdown(response)
    else:
        st.error("Please upload a PDF resume first.")