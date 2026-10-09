import os
import pyttsx3
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
import re
import warnings

warnings.filterwarnings("ignore")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

retriever = None
chunks = None


def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    return text


# -----------------------------
# PROCESS DOCUMENT
# -----------------------------

def process_document(file):

    global retriever
    global chunks

    # Save uploaded file
    with open(file.name, "wb") as f:
        f.write(file.getbuffer())

    # Load document
    if file.name.endswith("txt"):
        loader = TextLoader(file.name, encoding="latin-1")
    else:
        loader = PyPDFLoader(file.name)

    document = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=250
    )

    chunks = text_splitter.split_documents(document)
    chunks = [clean_text(text.page_content) for text in chunks]

    metadata = []

    for doc in document:
        metadata.append(doc.metadata)

    # Create vector DB
    db = Chroma.from_texts(
        texts=chunks,
        metadatas=metadata,
        embedding=embedding
    )

    retriever = db.as_retriever(search_kwargs={"k": 2})

    return len(chunks)


# -----------------------------
# ASK QUESTION
# -----------------------------

def ask_question(query):

    docs = retriever.invoke(query)

    relevant_chunks = []

    for doc in docs:
        relevant_chunks.append(doc.page_content)

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a document retrieval chatbot."),
        ("human", """
Use the following context to answer the question concisely and informatively in 10 lines

Context: {relevant_chunks}

Question: {query}
""")
    ])

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke({
        "relevant_chunks": relevant_chunks,
        "query": query
    })

    return response, relevant_chunks