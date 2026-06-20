from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

query = "How can I reset my password?"

results = vectorstore.similarity_search(
    query,
    k=3
)

print("\nRetrieved Documents:\n")

for doc in results:
    print(doc.metadata["source"])
    print(doc.page_content)
    print("-" * 50)