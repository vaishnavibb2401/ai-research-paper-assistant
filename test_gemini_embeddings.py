
import os
from dotenv import load_dotenv
from google import genai

# Load keys from .env
load_dotenv()

# Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Safety check
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Convert text into an embedding
response = client.models.embed_content(
    model="gemini-embedding-2",
    contents="Transformers use self-attention mechanisms."
)

vector = response.embeddings[0].values

print("Vector length:", len(vector))
print("First 10 values:", vector[:10])

print("\nGemini embedding test successful!")
