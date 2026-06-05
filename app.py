import streamlit as st
import os

from src.scraper import scrape_api_docs
from src.text_splitter import split_text_into_chunks
from src.vector_store import VectorStore
from src.rag_chain import answer_question_from_docs
from src.analyzer import analyze_api_docs
from src.code_generator import generate_python_wrapper

st.set_page_config(
    page_title="API Integration Copilot",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ API Integration Copilot")
st.write("A Smart DevTool that helps developers understand and integrate APIs faster.")

docs_url = st.text_input("Enter API Documentation URL")

use_case = st.text_area(
    "Describe your use case",
    placeholder="Example: I want to integrate payment checkout into my Python backend."
)

language = st.selectbox(
    "Preferred Programming Language",
    ["Python"]
)

st.divider()

if st.button("Scrape & Store Documentation"):
    if not docs_url:
        st.error("Please enter a documentation URL.")
    else:
        with st.spinner("Scraping and storing documentation..."):
            try:
                docs_text = scrape_api_docs(docs_url)

                os.makedirs("data", exist_ok=True)

                with open("data/scraped_docs.txt", "w", encoding="utf-8") as f:
                    f.write(docs_text)

                chunks = split_text_into_chunks(docs_text)

                vector_store = VectorStore()
                vector_store.add_documents(chunks)

                st.success("Documentation scraped, chunked, and stored successfully!")

                st.write(f"Total characters scraped: {len(docs_text)}")
                st.write(f"Total chunks created: {len(chunks)}")

                st.subheader("Preview")
                st.text_area("Scraped Content", docs_text[:5000], height=300)

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.subheader("Ask Questions About the API Docs")

question = st.text_input(
    "Ask a question",
    placeholder="Example: How do I authenticate requests?"
)

if st.button("Ask AI"):
    if not question:
        st.error("Please enter a question.")
    else:
        with st.spinner("Searching docs and generating answer..."):
            try:
                answer = answer_question_from_docs(question)
                st.success("Answer generated!")
                st.write(answer)

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.subheader("API Integration Analyzer")

if st.button("Analyze API Documentation"):
    if not use_case:
        st.error("Please describe your use case first.")
    else:
        with st.spinner("Analyzing API documentation..."):
            try:
                analysis = analyze_api_docs(use_case)
                st.success("API analysis completed!")
                st.markdown(analysis)

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.subheader("Python Wrapper Code Generator")

if st.button("Generate Python Wrapper"):
    if not use_case:
        st.error("Please describe your use case first.")
    else:
        with st.spinner("Generating Python wrapper code..."):
            try:
                wrapper_code = generate_python_wrapper(use_case)

                os.makedirs("generated", exist_ok=True)

                with open("generated/api_wrapper.py", "w", encoding="utf-8") as f:
                    f.write(wrapper_code)

                st.success("Python wrapper generated successfully!")

                st.code(wrapper_code, language="python")

                st.download_button(
                    label="Download api_wrapper.py",
                    data=wrapper_code,
                    file_name="api_wrapper.py",
                    mime="text/x-python"
                )

            except Exception as e:
                st.error(f"Error: {e}")


                