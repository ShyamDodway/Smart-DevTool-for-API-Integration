from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import GROQ_API_KEY, MODEL_NAME
from src.vector_store import VectorStore


def generate_python_wrapper(use_case: str) -> str:
    vector_store = VectorStore()

    search_query = f"""
    API authentication endpoints methods request response examples Python integration {use_case}
    """

    relevant_chunks = vector_store.search(search_query, top_k=10)
    context = "\n\n".join(relevant_chunks)

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0.1
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a senior Python SDK engineer.

Generate a ready-to-use Python wrapper class for the API based ONLY on the documentation context.

User Use Case:
{use_case}

Documentation Context:
{context}

Requirements:
- Generate clean Python code only.
- Use the requests library.
- Include a class name based on the API.
- Include __init__ with base_url and auth token/api key if needed.
- Include headers setup.
- Include methods for the most relevant endpoints.
- Include error handling with response.raise_for_status().
- Include JSON request/response handling.
- Add short comments where useful.
- Do not invent endpoints if they are not present in the context.
- If endpoint details are missing, add TODO comments.

Return only Python code.

Python Wrapper:
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "use_case": use_case,
        "context": context
    })

    return response.content

    