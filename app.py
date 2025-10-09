import streamlit as st
import openai
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_cover_letter(api_key, cv_text, job_description):
    client = openai.OpenAI(api_key=api_key)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates professional cover letters."
        },
        {
            "role": "user",
            "content": f"""
            Based on the following CV and job description, please generate a professional cover letter.

            **CV:**
            {cv_text}

            **Job Description:**
            {job_description}
            """
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

st.title("AI Cover Letter Generator")

api_key = os.getenv("OPENAI_API_KEY")

uploaded_cv = st.file_uploader("Upload your CV (PDF):", type=["pdf"])
job_description = st.text_area("Paste the Job Description here:")

if st.button("Generate Cover Letter"):
    if api_key and uploaded_cv and job_description:
        with st.spinner("Generating your cover letter..."):
            try:
                cv_text = extract_text_from_pdf(uploaded_cv)
                cover_letter = generate_cover_letter(api_key, cv_text, job_description)
                st.subheader("Generated Cover Letter:")
                st.write(cover_letter)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill in all the fields.")
