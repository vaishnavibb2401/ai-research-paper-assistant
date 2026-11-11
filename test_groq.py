from dotenv import load_dotenv
from langchain_groq import ChatGroq
# read the api api key from .env
load_dotenv()
# connect to the groq model 

llm = ChatGroq(
    model = "qwen/qwen3.8-27b",
   temperature=0
   )
# send a test question 

response = llm.invoke(
    "explain RAG in three  bullte simple sentence "
)
print(response.content)
