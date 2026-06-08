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
st.caption("Smart DevTool for faster API understanding, RAG-based Q&A, and Python wrapper generation.")

with st.sidebar:
    st.header("Project Controls")

    docs_url = st.text_input(
        "API Documentation URL",
        placeholder="https://jsonplaceholder.typicode.com/guide/"
    )

    max_pages = st.slider(
        "Pages to crawl",
        min_value=1,
        max_value=15,
        value=5
    )

    language = st.selectbox(
        "Preferred Language",
        ["Python"]
    )

    use_case = st.text_area(
        "Use Case",
        placeholder="I want to build a Python client that creates posts, reads posts, updates posts, and deletes posts."
    )

    st.info(
        "Step 1: Scrape docs\n\n"
        "Step 2: Ask questions\n\n"
        "Step 3: Analyze API\n\n"
        "Step 4: Generate wrapper"
    )

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Scrape Docs",
    "💬 Ask Docs",
    "🔍 API Analysis",
    "🐍 Code Generator"
])

with tab1:
    st.subheader("Scrape and Store API Documentation")

    if st.button("Scrape & Store Documentation", use_container_width=True):
        if not docs_url:
            st.error("Please enter a documentation URL.")
        else:
            with st.spinner("Scraping, chunking, and storing documentation..."):
                try:
                    docs_text = scrape_api_docs(docs_url, max_pages=max_pages)

                    if not docs_text.strip():
                        st.error("No documentation text was scraped. Try another URL.")
                        st.stop()

                    os.makedirs("data", exist_ok=True)

                    with open("data/scraped_docs.txt", "w", encoding="utf-8") as f:
                        f.write(docs_text)

                    chunks = split_text_into_chunks(docs_text)

                    if not chunks:
                        st.error("No chunks were created from the documentation.")
                        st.stop()

                    vector_store = VectorStore()
                    vector_store.add_documents(chunks)

                    st.session_state["docs_loaded"] = True
                    st.session_state["last_docs_url"] = docs_url
                    st.session_state["chunks_count"] = len(chunks)

                    st.success("Documentation scraped and stored successfully!")

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Characters Scraped", len(docs_text))
                    col2.metric("Chunks Created", len(chunks))
                    col3.metric("Pages Crawled", max_pages)

                    st.subheader("Documentation Preview")
                    st.text_area(
                        "Scraped Content Preview",
                        docs_text[:5000],
                        height=350
                    )

                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("Ask Questions About API Documentation")

    if "docs_loaded" not in st.session_state:
        st.warning("Please scrape and store documentation first.")

    question = st.text_input(
        "Your Question",
        placeholder="What endpoints are available?"
    )

    if st.button("Ask AI", use_container_width=True):
        if "docs_loaded" not in st.session_state:
            st.error("Please scrape and store documentation before asking questions.")
        elif not question:
            st.error("Please enter a question.")
        else:
            with st.spinner("Retrieving relevant docs and generating answer..."):
                try:
                    result = answer_question_from_docs(question)

                    st.success("Answer generated!")
                    st.markdown(result["answer"])

                    sources = result.get("sources", [])

                    with st.expander("View retrieved documentation chunks"):
                        if not sources:
                            st.warning("No source chunks were retrieved.")
                        else:
                            for i, chunk in enumerate(sources, start=1):
                                st.markdown(f"### Source Chunk {i}")
                                st.write(chunk[:1000])

                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.subheader("API Integration Analysis")

    st.write("This analyzes authentication, endpoints, request format, and integration approach.")

    if "docs_loaded" not in st.session_state:
        st.warning("Please scrape and store documentation first.")

    if st.button("Analyze API Documentation", use_container_width=True):
        if "docs_loaded" not in st.session_state:
            st.error("Please scrape and store documentation before analysis.")
        elif not use_case:
            st.error("Please describe your use case first.")
        else:
            with st.spinner("Analyzing API documentation..."):
                try:
                    analysis = analyze_api_docs(use_case)
                    st.success("API analysis completed!")
                    st.markdown(analysis)

                except Exception as e:
                    st.error(f"Error: {e}")

with tab4:
    st.subheader("Python Wrapper Code Generator")

    st.write("Generate a ready-to-use Python wrapper class based on the documentation and your use case.")

    if "docs_loaded" not in st.session_state:
        st.warning("Please scrape and store documentation first.")

    if st.button("Generate Python Wrapper", use_container_width=True):
        if "docs_loaded" not in st.session_state:
            st.error("Please scrape and store documentation before generating wrapper.")
        elif not use_case:
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
                        mime="text/x-python",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"Error: {e}")