import streamlit as st
import pandas as pd
import openai
import fitz  # PyMuPDF
import docx
import os

st.title("🧠 ESG AI Report Generator")

# Upload Excel ESG data
excel_file = st.file_uploader("Upload ESG data (Excel)", type=["xlsx"])

# Upload policy/governance documents
uploaded_docs = st.file_uploader("Upload ESG policy documents", type=["pdf", "docx"], accept_multiple_files=True)

# Choose section
section = st.selectbox("Which section to generate?", ["Emissions", "Governance"])

# OpenAI API Key (You can also use st.secrets in production)
openai.api_key = "your-openai-api-key-here"

def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        d = docx.Document(file)
        return "\n".join(p.text for p in d.paragraphs)
    return ""

if st.button("⚡ Generate Report Section"):
    if not excel_file or not uploaded_docs:
        st.warning("Please upload both ESG data and documents.")
    else:
        # Read Excel
        df = pd.read_excel(excel_file, sheet_name=section)

        # Extract all text
        doc_text = "\n\n".join([extract_text(doc) for doc in uploaded_docs])

        # Prompt to OpenAI
        prompt = f"""
You are an ESG analyst writing a {section} disclosure using GRI standards.
Use this data:

{df.to_string(index=False)}

And these documents:

{doc_text[:1500]}  # truncate for token limits

Write a clear, ~150-word ESG report section.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        output = response.choices[0].message.content
        st.subheader("✍️ Draft Report")
        st.markdown(output)
        st.download_button("Download Text", output, file_name=f"{section.lower()}_report.txt")
