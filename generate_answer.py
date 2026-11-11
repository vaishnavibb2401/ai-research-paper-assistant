
import os
import chromadb

from dotenv import load_dotenv
from google import genai
from langchain_groq import ChatGroq


# 1. Load API keys
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not gemini_key or not groq_key:
    raise ValueError("Check your API keys in the .env file")


# 2. Connect to Gemini
embedding_client = genai.Client(api_key=gemini_key)


# 3. Connect to Groq LLM
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0
)


# 4. Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_collection(
    name="research_paper"
)


# 5. Ask the user a question
question = input("Ask a question about the research paper: ")


# 6. Convert question into embedding
response = embedding_client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)

question_embedding = response.embeddings[0].values


# 7. Retrieve relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

retrieved_chunks = results["documents"][0]

if not retrieved_chunks:
    raise ValueError("No relevant information found.")


# 8. Combine retrieved chunks
context = "\n\n".join(retrieved_chunks)


# 9. Create a prompt
prompt = f"""
You are an AI research paper assistant.

Answer the question using only the context below.

If the answer is not available in the context,
say: "I could not find this information in the research paper."

Explain in simple English.

Context:
{context}

Question:
{question}

Answer:
"""


# 10. Generate answer using Groq
answer = llm.invoke(prompt)


# 11. Display final answer
print("\nFinal Answer:\n")
print(answer.content)
