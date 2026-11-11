import os 
from dotenv import load_dotenv
from groq import groq 

load_dotenv()

# convert text into embeddings 
api_key =  os.getenv("GROQ_API_KEY")

if not api_key :
    raise ValueError("GROQ_API_KEY not found in .env file")

# Create the Groq client
client = groq(api_key=api_key)

# Why do we need client?
# Because we use client to make API requests.

# Embeddings.

