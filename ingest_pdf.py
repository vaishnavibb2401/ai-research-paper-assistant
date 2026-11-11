from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# find the pdf file 
pdf_path = Path("data/attention_is_all_you_need.pdf")

# check whether the pdf exists 
if not pdf_path.exists():
    raise FileNotFoundError(
        f"pdf not found :{pdf_path.resolve()}\n"
        "please download the pdf into the data folder "
    )

# load the pdf 
loader = PyPDFLoader(str(pdf_path))
documents = loader.load()

# display the number of pages 
print("total pages:",len(documents))

# display the first pages metadta
print("\n first page metadat")
print(documents[0].metadata)

# extract and disp;ay the first 1000 charaters 
first_page_text = documents[0].page_content

print("\n first page text:")
print(first_page_text[:1000])

# check whether text was extracted 
if not any(doc.page_content.strip() for doc in documents):
    raise ValueError("No text was extracted from the PDF.")

print("\npdf loaded sucessfully!!!!")
