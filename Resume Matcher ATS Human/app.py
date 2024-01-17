import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import google.generativeai as genai
import io

from PIL import Image

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))
import pdf2image
import base64


model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,pdf_content,prompt):
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text


def pdf_input_pipeline(uploaded_file):
    if uploaded_file:
        pdf_images = pdf2image.convert_from_bytes(uploaded_file.read())
        page_1 = pdf_images[0]

        img_bytes = io.BytesIO()
        page_1.save(img_bytes,format='JPEG')
        img_bytes= img_bytes.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data":base64.b64encode(img_bytes).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("File is not uploaded")
    

st.set_page_config(page_title="Resume Evaluator")
st.header("Resume ATS Evaluator")
job_desc = st.text_area("Job Descriptioh", key="input")
uploaded_file= st.file_uploader("Upload your resume here in pdf", type=["pdf"])

if uploaded_file:
    st.write("uploaded")

submit_1 = st.button("I want to know about my resume")

submit_2 = st.button("Find Percentage match")

input_prompt_1 = """
You are an experienced Technical Recruiter. Your task is to review the resume of applicants and match with the job description.\
Please share if the candidates profile aligns with the job description.
Highlight strengths and weknesses of the applicant in relation to the specified job description.
"""

input_prompt_2="""
You are a skilled Applicant Tracking System with deep understanding of the subject and ATS functionality.
Your job is to evaluate the resume against the provided job description. Please provide the percentage of resume match with job description.\
First output should be the percentage match, followed by keywords missing and final thoughts on it at the end.
"""

if submit_1 or submit_2:
    if uploaded_file:
        pdf_content = pdf_input_pipeline(uploaded_file)
        if submit_1:
            response = get_gemini_response(input_prompt_1,pdf_content,job_desc)
            st.subheader("Evaluation of strengths")
            st.write(response)
        elif submit_2:
            response = get_gemini_response(input_prompt_2,pdf_content,job_desc)
            st.subheader("The ATS evaluator")
            st.write(response)
    else:
        st.write("file missing, please upload the resume file in pdf")


