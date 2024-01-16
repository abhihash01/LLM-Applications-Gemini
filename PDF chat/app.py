import os
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from PyPDF2 import PdfReader

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_pdf_text(pdfs):
    text=""
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text= text + page.extract_text()
    return text

def extract_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def store_vectors(text_chunks):
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    faiss_store = FAISS.from_texts(text_chunks,embedding=gemini_embeddings)
    faiss_store.save_local("FAISS_store")

def get_conversational_chain():

    prompt_template = """ 
    Provide answer to the question from the given context in a detailed format.If the answer \
    is not available in the context, say "answer is not available in the context". Don't make up answers.
    Context: \n {context}? \n
    Question: \n {question} \n

    Answer:
    """

    chat_model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.5)
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context","question"])
    chain = load_qa_chain(chat_model,chain_type = "stuff", prompt=prompt)

    return chain

def input(question):
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    faiss_db = FAISS.load_local("FAISS_store",gemini_embeddings)
    docs = faiss_db.similarity_search(question)
    chain = get_conversational_chain()

    response = chain({"input_documents":docs, "question": question}, return_only_outputs= True)

    print(response)
    st.write("Response: ", response["output_text"])

def main():
    st.set_page_config("Gemini PDF Chat")
    st.header("PDF Chat")

    question = st.text_input("Question to look in the PDF Files")

    if question:
        input(question)
    
    with st.sidebar:
        st.title("Uploads ")
        pdfs = st.file_uploader("Upload PDFs", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("loading..."):
                raw_text = extract_pdf_text(pdfs)
                text_chunks = extract_text_chunks(raw_text)
                store_vectors(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()