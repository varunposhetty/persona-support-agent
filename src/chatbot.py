from dotenv import load_dotenv
from google import genai
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from persona_detector import detect_persona
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

query = input("User: ")

persona = detect_persona(query)

results = vectorstore.similarity_search(query, k=3)

context = ""

for doc in results:
    context += doc.page_content + "\n\n"

prompt = f"""
You are a customer support agent.

Customer Persona:
{persona}

Support Documents:
{context}

Customer Question:
{query}

Instructions:

Technical Expert:
- Detailed explanation
- Technical language
- Root cause analysis

Frustrated User:
- Empathetic
- Reassuring
- Simple language

Business Executive:
- Concise
- Business impact
- Resolution guidance

Only answer from the provided documents.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\nDetected Persona:", persona)

print("\nSources:")
for doc in results:
    print("-", doc.metadata["source"])

print("\nResponse:\n")
print(response.text)