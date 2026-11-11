
import os
import chromadb

from dotenv import load_dotenv
from google import genai


# 1. Load Gemini API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# 2. Connect to existing ChromaDB
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_collection(
    name="research_paper"
)

print("Total stored chunks:", collection.count())


# 3. Ask the user for a question
question = input("Ask a question about the research paper: ")


# 4. Convert question into an embedding
response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)

question_embedding = response.embeddings[0].values


# 5. Search for the 3 most relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)


# 6. Display retrieved chunks
print("\nRelevant information from the PDF:\n")

for i, text in enumerate(results["documents"][0]):

    print(f"\n--- Result {i + 1} ---")
    print(text)

    print("Metadata:", results["metadatas"][0][i])
    print("Distance:", results["distances"][0][i])
