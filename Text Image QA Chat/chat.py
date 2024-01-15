import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat_model = model.start_chat(history=[])
def get_gemini_response(prompt):
    response = chat_model.send_message(prompt, stream=True)
    return response

#streamlit

st.set_page_config(page_title="Chat")
st.header("Gemini Chat Applicaiton")

if 'history' not in st.session_state:
    st.session_state['history'] = []

prompt = st.text_input("Prompt", key="input")
submit = st.button("Chat now")

if submit:
    response = get_gemini_response(prompt)
    st.session_state['history'].append(("User:", prompt))
    st.subheader("The Model output")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['history'].append(("Model:",chunk.text))
#st.write(chat_model.history)
        
st.subheader("History")

for prompter,prompt_response in st.session_state['history']:
    st.write(f"{prompter}: {prompt_response}")