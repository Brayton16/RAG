import os 
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

VECTOR_STORE_PATH = "data/processed"

def load_retriever():
    try:
        if not os.path.exists(VECTOR_STORE_PATH):
            raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_PATH}")
        
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        return vector_store.as_retriever(search_kwargs={"k": 15})
    except Exception as e:
        print(f"Error loading retriever: {e}")
        return None