import streamlit as st
from google import genai
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.persona_detector import detect_persona
from src.escalation import should_escalate

# Gemini Client
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS Vector Store
vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

# UI
st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Persona Adaptive Support Agent")
st.write("Ask your support question:")

query = st.text_input(
    "",
    placeholder="Enter your support issue..."
)

if query:

    # Detect Persona
    persona = detect_persona(query)

    # Retrieve Documents
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

Response Style:

Technical Expert:
- Detailed technical explanation.
- Include troubleshooting steps.

Frustrated User:
- Empathetic response.
- Reassure the customer.

Business Executive:
- Focus on business impact.
- Mention timelines and risks.

Only answer using the support documents.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    st.write("## Detected Persona")
    st.success(persona)

    st.write("## Retrieved Sources")

    for doc in results:
        st.write(f"• {doc.metadata['source']}")

    st.write("## Response")
    st.write(response.text)

    if should_escalate(query, results):
        st.error("⚠ Escalation Required")
    else:
        st.success("✅ No Escalation Required")