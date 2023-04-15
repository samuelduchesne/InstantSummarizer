import streamlit as st
import pdfplumber
import openai
import io
import os
from PIL import Image

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages)
    return text

def summarize(api_key, document):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Please summarize the following document:\n\n{document}\n",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary

st.set_page_config(page_title="PDF Summarizer", layout="wide")
st.title("PDF Summarizer")

api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text(uploaded_file)

    if extracted_text:
        with st.spinner("Summarizing document..."):
            summary = summarize(api_key, extracted_text)
        st.write(summary)
    else:
        st.warning("Could not extract text from the uploaded PDF.")
else:
    st.warning("Please upload a PDF file.")
