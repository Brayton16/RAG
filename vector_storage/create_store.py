import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

DATA_DIR = "data/raw_papers"
OUTPUT_DIR = "data/processed"

def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    return documents

def build_vector_store():
    total_docs = 0
    all_split_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    embeddings = OpenAIEmbeddings()

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            file_path = os.path.join(DATA_DIR, filename)
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            split_docs = text_splitter.split_documents(docs)
            all_split_docs.extend(split_docs)

            print(f"📄 {filename} → {len(docs)} páginas → {len(split_docs)} fragmentos")

            total_docs += len(split_docs)

    if not all_split_docs:
        raise ValueError("No documents found or no content to split.")

    vector_store = FAISS.from_documents(all_split_docs, embeddings)
    vector_store.save_local(OUTPUT_DIR)

    print(f"\n✅ Total de fragmentos almacenados en FAISS: {total_docs}")

    