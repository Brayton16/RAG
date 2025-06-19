# from vector_storage.retriever import load_retriever
# from langgraph_app.graph_builder import GraphState
# retriever = load_retriever()
from typing import TypedDict, Optional, List
from vector_storage.retriever import load_retriever
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.documents import Document

class GraphState(TypedDict):
    prompt: str
    result: Optional[str]
    __next__: Optional[str]
    __queue__: List[str]


def agente_resumen_node(state: GraphState) -> GraphState:
    # prompt = state.get("prompt", "")
    # docs = retriever.get_relevant_documents(prompt)
    
    # content = "\n".join([doc.page_content for doc in docs[:3]])
    # summary = f"Resumen de los documentos:\n{content}\n\n"

    # state["result"] = summary  # Cambiar a "result", no "response"
    # return state
    print("Generando resumen a partir del prompt...")
    return state

def nodo_resumen(state: GraphState) -> GraphState:
    print("🔹 Nodo RESUMEN ejecutado")

    retriever = load_retriever()
    if not retriever:
        print("⚠️ No se pudo cargar el recuperador de documentos.")
        state["result"] = (state.get("result", "") or "") + "\n[Error: No se pudo cargar el retriever]"
        state["__next__"] = state.get("__queue__", []).pop(0) if state.get("__queue__") else None
        return state

    docs = retriever.invoke(state["prompt"])
    if not docs:
        print("⚠️ No se encontraron documentos relevantes.")
        state["result"] = (state.get("result", "") or "") + "\n[Error: No se encontraron documentos relevantes]"
        state["__next__"] = state.get("__queue__", []).pop(0) if state.get("__queue__") else None
        return state

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.5,
        max_tokens=1000,
        top_p=0.9,
        frequency_penalty=0.3,
        presence_penalty=0.4
    )

    prompt = ChatPromptTemplate.from_template(
        "Eres un asistente de investigación. Resume el siguiente contenido académico en español:\n\n{context}"
    )

    chain = RunnableMap({
        "context": lambda _: "\n\n".join(doc.page_content for doc in docs)
    }) | prompt | llm

    respuesta = chain.invoke({"prompt": state["prompt"]})

    state["result"] = (state.get("result", "") or "") + "\n🔹 Resumen:\n" + respuesta.content
    state["__next__"] = state.get("__queue__", []).pop(0) if state.get("__queue__") else None
    return state