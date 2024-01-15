import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#loading Gemini Model for text

model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question):
    response=model.generate_content(question)
    return response.text

#streamlit set up

st.set_page_config(page_title="Demo")

st.header("LLM Application Gemini")

input = st.text_input("Input", key="input")
submit = st.button("Submit Question")


#on submit

if submit:
    response = get_gemini_response(input)
    st.subheader("The Response")
    st.write(response)