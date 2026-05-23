import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.title("AI Document Summarizer")

text = st.text_area(
    "Paste your document text here",
    height=300
)

if st.button("Summarize"):

    if text:

        with st.spinner("Generating summary..."):

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"""
                Summarize this professionally in concise bullet points:

                {text}
                """
            )

            st.subheader("Summary")
            st.write(response.text)

    else:
        st.warning("Please enter some text.")