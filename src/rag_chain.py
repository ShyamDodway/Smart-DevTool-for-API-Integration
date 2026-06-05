from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import GROQ_API_KEY, MODEL_NAME
from src.vector_store import VectorStore


def answer_question_from_docs(question: str) -> str:
    vector_store = VectorStore()

    relevant_chunks = vector_store.search(question, top_k=5)

    context = "\n\n".join(relevant_chunks)

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an API documentation assistant.

Answer the user's question using ONLY the documentation context below.

If the answer is not available in the context, say:
"I could not find this information in the provided documentation."

Documentation Context:
{context}

User Question:
{question}

Answer:
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content