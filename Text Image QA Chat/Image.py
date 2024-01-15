import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import google.generativeai as genai

from PIL import Image
import pathlib
import textwrap


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#loading Gemini Model for text

model = genai.GenerativeModel("gemini-pro-vision")
def get_gemini_response(prompt,image):
    if prompt!="":
        response = model.generate_content([prompt,image])
    else:
        response = model.generate_content(image)
    return response.text

#streamlit set up

st.set_page_config(page_title="Gemini Image")

st.header("Image Application Gemini")

prompt = st.text_input("Prompt", key="input")
file = st.file_uploader("Select Image", type=["png","jpg","jpeg"])

if file:
    image=Image.open(file)
    st.image(image, caption = "Given Image", use_column_width=True)

submit = st.button("Ask my question with the prompt and image")


#on submit

if submit:
    response = get_gemini_response(prompt,image)
    if prompt=="":
        st.subheader("About the image")
    else:
        st.subheader("About the prompt and Image")
    st.write(response)