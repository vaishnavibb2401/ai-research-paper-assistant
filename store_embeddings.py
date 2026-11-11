import json 
import chromadb 

# load saved embeddings 
with open("embeddings_progress.json", "r", encoding="utf-8") as file:
    saved_data = json.load(file)

print("total records:",len(saved_data))

# check that all 66 embeddings are avilable

if len(saved_data)!=66:
    raise ValueError("expected 66 embeddings. please check your json file")

client = chromadb.PersistentClient(path = "chroma_db")

# create or acess a collection 
collection = client.get_or_create_collection(
    name="research_paper",
    metadata={"hnsw:space": "cosine"}
)

# prepare data for chromadb 

ids = [f"chunk-{i}"for i in range(len(saved_data))]

texts = [item["text"]for item in saved_data]

embeddings = [item["embedding"]for item in saved_data]

metadatas = [item["metadata"]for item in saved_data]

# store everything in chromadb
collection.upsert(
    ids= ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)

# verify stored records 
print("total records stored :",collection.count())
print("chromadb storage sucessfull!")
