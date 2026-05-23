import streamlit as st
from transformers import pipeline

st.title("AI Document Summarizer")

@st.cache_resource
def load_model():
    return pipeline(
        task="summarization",
        model="google/pegasus-xsum"
    )

summarizer = load_model()

text = st.text_area(
    "Paste your document text here",
    height=300
)

if st.button("Summarize"):

    if text:

        with st.spinner("Generating summary..."):

            prompted_text = f"""
            Summarize the following text professionally in bullet points:

            {text}
            """

            result = summarizer(
                prompted_text[:1000],
                max_length=120,
                min_length=40,
                do_sample=False
            )

            st.subheader("Summary")
            st.write(result[0]["summary_text"])

    else:
        st.warning("Please enter some text.")
        
# import streamlit as st
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# st.title("AI Document Summarizer")

# text = st.text_area(
#     "Paste your document text here",
#     height=300
# )

# if st.button("Summarize"):

#     if text:

#         with st.spinner("Generating summary..."):

#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": f"Summarize this document:\n{text}"
#                     }
#                 ]
#             )

#             summary = response.choices[0].message.content

#             st.subheader("Summary")
#             st.write(summary)

#     else:
#         st.warning("Please enter some text.")