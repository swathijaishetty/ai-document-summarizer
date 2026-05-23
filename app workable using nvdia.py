import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2

# Load environment variables
load_dotenv()

# OpenRouter client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Streamlit page config
st.set_page_config(
    page_title="AI Document Summarizer",
    page_icon="🧠",
    layout="centered"
)

# App title
st.title("🧠 AI Document Summarizer")

st.write(
    "Upload a PDF or paste text to generate AI-powered summaries."
)

# Summary type selector
summary_type = st.selectbox(
    "Choose Summary Type",
    [
        "Bullet Points",
        "Short Summary",
        "Detailed Summary"
    ]
)

# PDF Upload
uploaded_file = st.file_uploader(
    "Upload PDF File",
    type=["pdf"]
)

# Text area input
text = st.text_area(
    "Or paste your document text here",
    height=300
)

# Extract text from PDF
pdf_text = ""

if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        extracted_text = page.extract_text()

        if extracted_text:
            pdf_text += extracted_text

    st.success("✅ PDF uploaded successfully!")

# Final text source
final_text = pdf_text if pdf_text else text

# Generate prompts dynamically
def generate_prompt(summary_type, content):

    if summary_type == "Bullet Points":

        return f"""
        You are a professional AI document summarizer.

        Read the following document carefully and provide:
        - concise bullet point summary
        - key insights
        - important decisions
        - action items if present

        Document:
        {content}
        """

    elif summary_type == "Short Summary":

        return f"""
        Provide a short professional summary of the following document
        in 5-6 clear lines.

        Document:
        {content}
        """

    else:

        return f"""
        Provide a detailed professional summary of the following document.

        Include:
        - major points
        - insights
        - conclusions
        - recommendations if present

        Document:
        {content}
        """

# Summarize button
if st.button("Summarize"):

    if final_text:

        with st.spinner("Generating summary..."):

            try:

                # Limit huge documents
                trimmed_text = final_text[:12000]

                # Generate dynamic prompt
                prompt = generate_prompt(
                    summary_type,
                    trimmed_text
                )

                # API call
                response = client.chat.completions.create(

                    model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                # Extract summary
                summary = response.choices[0].message.content

                # Display summary
                st.subheader("📄 Summary")

                st.markdown(summary)

                # Download button
                st.download_button(
                    label="⬇ Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

            except Exception as e:

                st.error(f"❌ Error: {e}")

    else:

        st.warning(
            "⚠ Please upload a PDF or enter some text."
        )