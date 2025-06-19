import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

RAW_DIR = "data/raw_papers"
VECTOR_STORE_DIR = "data/processed"

def ingest_pdf(pdf_path: str):
    filename = os.path.basename(pdf_path)
    new_path = os.path.join(RAW_DIR, filename)

    # ✅ 0. Limpiar carpeta raw_papers
    if os.path.exists(VECTOR_STORE_DIR):
        limpiar_carpeta(VECTOR_STORE_DIR)
        print("Directorios removidos")

    # ✅ 1. Copiar el PDF al folder solo si está en una ubicación distinta
    if os.path.abspath(pdf_path) != os.path.abspath(new_path):
        shutil.copy2(pdf_path, new_path)
        print(f"📂 PDF copiado a {new_path}")
    else:
        print(f"📂 El PDF ya está en {new_path}, no se copia.")

    # ✅ 2. Procesar solo este PDF
    loader = PyPDFLoader(new_path)
    documents = loader.load()
    print(f"📄 Cargadas {len(documents)} páginas del PDF.")

    # ✅ 3. Fragmentar texto
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)
    print(f"✂️ Fragmentados en {len(docs)} fragmentos de texto.")

    # ✅ 4. Cargar o crear FAISS
    embeddings = OpenAIEmbeddings()
    index_file = os.path.join(VECTOR_STORE_DIR, "index.faiss")
    pkl_file = os.path.join(VECTOR_STORE_DIR, "index.pkl")

    if os.path.exists(index_file) and os.path.exists(pkl_file):
        vectorstore = FAISS.load_local(VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(docs)
        print("📥 Vector store existente cargado y actualizado.")
    else:
        vectorstore = FAISS.from_documents(docs, embeddings)
        print("📦 Vector store creado desde cero.")

    vectorstore.save_local(VECTOR_STORE_DIR)
    print("✅ Vector store actualizado con éxito.")

def limpiar_carpeta(ruta_carpeta):
    """
    Elimina todos los archivos dentro de una carpeta,
    pero no la carpeta en sí.

    Args:
        ruta_carpeta: La ruta de la carpeta a limpiar.
    """
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        try:
            if os.path.isfile(ruta_completa):
                os.remove(ruta_completa)
            # Si necesitas eliminar también subcarpetas y sus contenidos
            #  elimina esta línea y descomenta la siguiente:
            # elif os.path.isdir(ruta_completa):
            #    shutil.rmtree(ruta_completa)
        except Exception as e:
            print(f"Error al eliminar {ruta_completa}: {e}")