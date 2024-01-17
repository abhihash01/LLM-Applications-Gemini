import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import google.generativeai as genai

from PIL import Image

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def image_pipeline(image_file):
    if image_file:
        image_bytes = image_file.getvalue()

        image_parts = [
            {
                "mime_type": image_file.type,
                "data": image_bytes
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Upload File Please")
    
#streamlit
    
st.set_page_config(page_title="Invoice Information Extractor")

st.header("Gemini Invoice Extractor")

input = st.text_input("Instructions to the Calorie Calculator", key="input")
image_file = st.file_uploader("Select Image", type=["png","jpg","jpeg"])


if image_file:
    image = Image.open(image_file)
    st.image(image,caption="Here is the image", use_column_width = True)


submit= st.button("Ask Question")

input_prompt="""
You are expert on understanding invoices in all languages. Use the uploaded image as invoice \
    and answer the questions that we ask about the invoice correctly"""

if submit:
    image_data = image_pipeline(image_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("Here is the invoice information")
    st.write(response)