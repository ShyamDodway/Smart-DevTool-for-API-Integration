from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import GROQ_API_KEY, MODEL_NAME
from src.vector_store import VectorStore


def analyze_api_docs(use_case: str) -> str:
    vector_store = VectorStore()

    search_query = f"""
    authentication authorization endpoints API methods base URL request response {use_case}
    """

    relevant_chunks = vector_store.search(search_query, top_k=8)
    context = "\n\n".join(relevant_chunks)

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0.1
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a senior API integration engineer.

Analyze the API documentation context and produce a clear integration summary.

Use ONLY the provided context. If something is missing, write "Not clearly found in docs."

User Use Case:
{use_case}

Documentation Context:
{context}

Return the answer in this format:

# API Integration Analysis

## 1. API Purpose
Explain what this API is used for.

## 2. Authentication Method
Explain authentication method, required tokens, headers, API keys, OAuth, or bearer token if available.

## 3. Key Endpoints
Create a table with:
- HTTP Method
- Endpoint / Path
- Purpose
- Important Parameters

## 4. Request and Response Format
Explain whether it uses JSON, REST, headers, query params, body params, etc.

## 5. Recommended Integration Path
Explain whether the user should use REST calls, SDK, OAuth flow, API key, webhook, etc.

## 6. Risks / Missing Information
Mention any missing information or things the developer must verify.

Answer:
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "use_case": use_case,
        "context": context
    })

    return response.content

    