from langchain.schema.runnable import RunnableMap
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from vector_storage.retriever import load_retriever
from typing import TypedDict, Optional, List

class GraphState(TypedDict):
    prompt: str
    result: Optional[str]
    __next__: Optional[str]
    __queue__: List[str]


def agente_escritura_node(state: GraphState) -> GraphState:
    # prompt = state["prompt"]

    # generated_text = f"""
    # Esta es una introducción generada automáticamente a partir del siguiente prompt:
    # "{prompt[:100]}..."

    # La inteligencia artificial ha transformado radicalmente la forma en que se realiza la investigación académica.
    # """
    # return {
    #     "result": generated_text.strip()
    # }
    # Simulación de generación de texto
    print("Generando texto a partir del prompt...")
    return state

def nodo_escritura(state: GraphState) -> GraphState:
    print("🟩 Nodo ESCRITURA ejecutado")

    retriever = load_retriever()
    if not retriever:
        print("⚠️ No se pudo cargar el recuperador de documentos.")
        state["result"] = (state.get("result", "") or "") + "\n[Error: No se pudo cargar el retriever]"
        state["__next__"] = state["__queue__"].pop(0) if state.get("__queue__") else None
        return state

    docs = retriever.invoke(state["prompt"])
    if not docs:
        print("⚠️ No se encontraron documentos relevantes.")
        state["result"] = (state.get("result", "") or "") + "\n[Error: No se encontraron documentos relevantes]"
        state["__next__"] = state["__queue__"].pop(0) if state.get("__queue__") else None
        return state

    # Preparar el LLM y prompt
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7, 
        max_tokens=1000,
        top_p=0.9,
        frequency_penalty=0.3,
        presence_penalty=0.4
        
    )

    prompt = ChatPromptTemplate.from_template(
        "Actúa como un asistente de investigación con experiencia en redacción académica en español. "
        "Utiliza el siguiente contexto extraído de fuentes académicas:\n\n{context}\n\n"
        "Con base en este contenido:\n"
        "1. Escribe una introducción académica clara, formal y concisa (150 a 200 palabras).\n"
        "2. Utiliza voz en tercera persona y evita expresiones subjetivas.\n"
        "3. Integra al menos una cita textual entre comillas, referenciada al final con el formato (Apellido, año).\n"
        "4. Finaliza con una oración de cierre que indique la estructura del texto completo.\n"
        "No inventes información. Si no hay suficiente contexto, indícalo explícitamente."
    )

    # Runnable chain moderno
    chain = RunnableMap({
        "context": lambda _: "\n\n".join([doc.page_content for doc in docs]),
    }) | prompt | llm

    respuesta = chain.invoke({"prompt": state["prompt"]})

    state["result"] = (state.get("result", "") or "") + "\n🟩 Introducción generada:\n" + respuesta.content
    state["__next__"] = state["__queue__"].pop(0) if state.get("__queue__") else None
    return state

