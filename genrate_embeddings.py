
import os
import json
import time

from dotenv import load_dotenv
from google import genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. Connect to Gemini
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# 2. Load PDF
loader = PyPDFLoader("data/attention_is_all_you_need.pdf")
documents = loader.load()


# 3. Create chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(documents)

print("Total chunks:", len(chunks))


# 4. Load previously saved embeddings
file_name = "embeddings_progress.json"

if os.path.exists(file_name):
    with open(file_name, "r") as file:
        saved_data = json.load(file)
else:
    saved_data = []


# 5. Generate remaining embeddings
for i in range(len(saved_data), len(chunks)):

    try:
        response = client.models.embed_content(
            model="gemini-embedding-2",
            contents=chunks[i].page_content
        )

        vector = response.embeddings[0].values

        saved_data.append({
            "text": chunks[i].page_content,
            "metadata": chunks[i].metadata,
            "embedding": vector
        })

        # Save immediately
        with open(file_name, "w") as file:
            json.dump(saved_data, file)

        print("Completed:", len(saved_data), "/", len(chunks))

        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        print("Saved progress:", len(saved_data), "/", len(chunks))
        break


print("\nTotal embeddings saved:", len(saved_data))
