# 🎙️ Voice Assistant RAG

A Retrieval-Augmented Generation (RAG) powered voice assistant that allows users to upload PDF or text documents, ask questions using their voice, and receive spoken answers generated from the document's content. The application combines speech recognition, semantic search, vector databases, and large language models to provide accurate, context-aware responses.

---

## 🚀 Features

* 📄 Upload **PDF** and **TXT** documents
* ✂️ Automatic document chunking for efficient retrieval
* 🧠 Semantic search using **Hugging Face sentence embeddings**
* 🗂️ Vector storage with **ChromaDB**
* 🤖 LLM answer generation using the **Gemini API**
* 🎤 Voice-based question input
* 🔊 Text-to-speech response generation
* 💻 Interactive Streamlit interface
* ⚡ Local document processing, embeddings and vector store; only answer generation calls the Gemini API

---

## 🛠️ Tech Stack

| Category           | Technologies                    |
| ------------------ | ------------------------------- |
| Frontend           | Streamlit                       |
| Backend            | Python                          |
| LLM                | Google Gemini API               |
| Framework          | LangChain                       |
| Embeddings         | Hugging Face `all-MiniLM-L6-v2` |
| Vector Database    | ChromaDB                        |
| Speech Recognition | SpeechRecognition               |
| Text-to-Speech     | pyttsx3                         |
| Document Loaders   | PyPDFLoader, TextLoader         |

---

## 📌 System Architecture

```
                +------------------+
                | Upload Document  |
                +--------+---------+
                         |
                         v
               Document Processing
                         |
                         v
        Recursive Text Chunking
                         |
                         v
      Hugging Face Embeddings
                         |
                         v
          Chroma Vector Database
                         |
                         |
Voice Query ---> Speech Recognition
                         |
                         v
                 Semantic Retrieval
                         |
                         v
                  Gemini API
                         |
                         v
                Generated Response
                         |
                         v
                 Text-to-Speech
                         |
                         v
                  Audio Response
```

---

## 📂 Project Structure

```
Voice-Assistant-RAG/
│
├── app.py                  # Backend RAG pipeline
├── frontend.py             # Streamlit application
├── requirements.txt
├── README.md
└── sample_documents/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Voice-Assistant-RAG.git
cd Voice-Assistant-RAG
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Create an API key in [Google AI Studio](https://aistudio.google.com/apikey) and set it as an environment variable:

**Windows (PowerShell)**

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Linux / macOS**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

The model defaults to `gemini-2.5-flash`; override it with the `GEMINI_MODEL` environment variable.

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run frontend.py
```

---

## 📖 How It Works

1. Upload a PDF or TXT document.
2. The document is split into overlapping text chunks.
3. Each chunk is converted into vector embeddings.
4. Embeddings are stored in a Chroma vector database.
5. Ask a question using your microphone.
6. The query is converted to text.
7. Relevant document chunks are retrieved using semantic similarity.
8. Retrieved context is provided to the Gemini model.
9. The generated answer is converted into speech and played back.

---

## 🎯 Example Workflow

```
Upload PDF
      │
      ▼
Process Document
      │
      ▼
Click "Start Recording"
      │
      ▼
Ask Your Question
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Generate Answer with Gemini
      │
      ▼
Play Audio Response
```

---

## 💡 Future Improvements

* Support multiple document uploads
* Persistent vector database
* Chat history and conversational memory
* Streaming LLM responses
* Source citations with page numbers
* Whisper-based offline speech recognition
* Natural-sounding neural text-to-speech
* Docker deployment
* FastAPI backend with React frontend
* Hybrid retrieval (BM25 + semantic search)

---

## 📚 Key Concepts Demonstrated

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Embeddings
* Document Chunking
* Large Language Models
* Voice Interfaces
* Cloud LLM APIs (Gemini)
* Vector Databases

---

