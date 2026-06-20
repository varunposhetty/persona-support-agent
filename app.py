import streamlit as st
from dotenv import load_dotenv
from google import genai
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.persona_detector import detect_persona
from src.escalation import should_escalate
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

st.title("🤖 Persona Adaptive Support Agent")

query = st.text_input("Ask your support question:")

if query:

    persona = detect_persona(query)

    results = vectorstore.similarity_search(query, k=3)

    context = ""

    for doc in results:
        context += doc.page_content + "\n\n"

    prompt = f"""
Customer Persona: {persona}

Support Documents:
{context}

Customer Question:
{query}

Technical Expert:
- Detailed explanation.

Frustrated User:
- Empathetic response.

Business Executive:
- Business impact focused.

Only answer from the documents.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    st.write("### Detected Persona")
    st.write(persona)

    st.write("### Retrieved Sources")

    for doc in results:
        st.write("•", doc.metadata["source"])

    st.write("### Response")
    st.write(response.text)

    if should_escalate(query, results):
        st.error("Escalation Required")
    else:
        st.success("No Escalation Required")