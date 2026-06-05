import streamlit as st
import os

from src.scraper import scrape_api_docs

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

if st.button("Scrape Documentation"):
    if not docs_url:
        st.error("Please enter a documentation URL.")
    else:
        with st.spinner("Scraping documentation..."):
            try:
                docs_text = scrape_api_docs(docs_url)

                os.makedirs("data", exist_ok=True)

                with open("data/scraped_docs.txt", "w", encoding="utf-8") as f:
                    f.write(docs_text)

                st.success("Documentation scraped successfully!")
                st.subheader("Preview")
                st.text_area("Scraped Content", docs_text[:5000], height=400)

            except Exception as e:
                st.error(f"Error while scraping: {e}")