from pathlib import Path 

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# load the pdf 
pdf_path = Path("data/attention_is_all_you_need.pdf")

if not pdf_path.exists():
    raise FileNotFoundError(
        f'pdf not found :{pdf_path.resolve()}'
    )

loader = PyPDFLoader(str(pdf_path))
documents = loader.load()

print("total pages :",len(documents))

# creates the text splitter 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800,
    chunk_overlap = 150
)

# split the documents into chunks 
chunks = text_splitter.split_documents(documents)

# display the number of chunks 
print("total chunks:",len(chunks))

# display the first chunk 
print("\n first chunk ")
print(chunks[0].page_content)

# display the first chunks metadata 
print("\n first chunk metadata")
print(chunks[0].metadata)

# display the length of first chunk 
print("\n first chunk characters :")
print(len(chunks[0].page_content))

print("\n text splitting completed sucessfully!")