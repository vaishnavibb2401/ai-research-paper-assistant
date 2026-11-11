# 📚 AI Research Paper Assistant

An AI-powered PDF chatbot built using **Retrieval-Augmented Generation (RAG)**. It allows users to ask questions about a research paper and receive context-based answers with source citations.

## 🚀 Project Overview

The AI Research Paper Assistant helps users understand research papers through a conversational interface.

Users can:
- Upload or work with a research paper PDF.
- Ask questions about the paper.
- Retrieve relevant information using semantic search.
- Generate answers using an LLM.
- View source page numbers and retrieved text.
- Access previous chat conversations.

## 🏗️ Architecture

1. **PDF Loading:** Extract text from PDF documents using PyPDFLoader.
2. **Text Splitting:** Split extracted text into smaller chunks using RecursiveCharacterTextSplitter.
3. **Embeddings:** Convert text chunks into vector embeddings using Gemini.
4. **Vector Database:** Store embeddings and metadata in ChromaDB.
5. **Retrieval:** Find relevant chunks based on the user's question.
6. **Answer Generation:** Use Groq LLM to generate answers based on retrieved context.
7. **Source Citations:** Display source page numbers and relevant PDF text.
8. **Chat History:** Save and restore previous conversations.

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Google Gemini Embeddings
- Groq API
- ChromaDB
- PyPDF
- Python-dotenv

## 📂 Project Structure

```text
AI-Research-Paper-Assistant/
│
├── app.py
├── chat_db.py
├── ingest_pdf.py
├── split_text.py
├── store_embeddings.py
├── retrieve_chunks.py
├── generate_answer.py
├── embedding_test.py
├── test_gemini_embeddings.py
├── test_groq.py
│
├── data/
│   └── attention_is_all_you_need.pdf
│
├── chroma_db/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/vaishnavibb2401/ai-research-paper-assistant.git
```

### 2. Navigate to the project folder

```bash
cd ai-research-paper-assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

Never upload your `.env` file or API keys to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

## ✨ Key Features

- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- Context-based answer generation
- Source citations with page numbers
- Persistent chat history
- Interactive Streamlit interface
- API error handling

## 🎯 Learning Outcomes

Through this project, I gained practical experience with:

- Building an end-to-end RAG pipeline.
- Working with embedding models.
- Storing and retrieving vectors using ChromaDB.
- Integrating LLM APIs.
- Developing an interactive chatbot using Streamlit.
- Managing chat history and source citations.


GitHub: [vaishnavibb2401](https://github.com/vaishnavibb2401)

*This project was developed to explore practical applications of Generative AI and Retrieval-Augmented Generation.*
