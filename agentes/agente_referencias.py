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


def agente_referencias_node(state: GraphState) -> GraphState:
    # prompt = state["prompt"]

    # # Usamos un hash para simular un ID único por entrada
    # hash_id = hashlib.md5(prompt.encode()).hexdigest()[:6]

    # # Simulación de generación de referencia en formato IEEE
    # reference = f"[1] A. Author, “Title related to: {prompt[:40]}...”, Journal of Simulated Research, vol. 10, no. 2, pp. 100–110, 2024. doi:10.1234/{hash_id}"

    # return {
    #     "result": reference
    # }
    print("Generando referencias a partir del prompt...")
    return state


def nodo_referencias(state: GraphState) -> GraphState:
    print("🟡 Nodo REFERENCIAS ejecutado")

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

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.2,
        max_tokens=1000,
        top_p=0.9,
        frequency_penalty=0.3,
        presence_penalty=0.4
    )

    prompt = ChatPromptTemplate.from_template(
        "Actúas como un asistente académico especializado en generación de referencias bibliográficas. "
        "A partir del siguiente contenido académico:\n\n{context}\n\n"
        "Genera referencias **reales o plausibles** directamente relacionadas con el texto anterior, en los siguientes formatos:\n"
        "• IEEE (mínimo 2 entradas)\n"
        "• APA 7 (mínimo 2 entradas)\n\n"
        "Requisitos:\n"
        "1. No repitas autores ni títulos.\n"
        "2. Si se menciona un autor, obra o publicación en el texto, intenta incluirla en las referencias.\n"
        "3. Evita referencias inventadas que suenen falsas. Si necesitas simularlas, hazlo de forma verosímil.\n"
        "4. Ordena cada lista alfabéticamente.\n"
        "5. Devuelve primero las referencias IEEE, luego las APA 7, con un encabezado claro para cada sección."
    )

    chain = RunnableMap({
        "context": lambda _: "\n\n".join(doc.page_content for doc in docs)
    }) | prompt_template | llm

    respuesta = chain.invoke({"prompt": state["prompt"]})
    texto = respuesta.content.strip()

    # Filtro opcional para evitar duplicados exactos
    referencias = list(dict.fromkeys(texto.split("\n")))
    texto_filtrado = "\n".join(referencias)

    state["result"] = (state.get("result", "") or "") + "\n🟡 Referencias:\n" + texto_filtrado
    state["__next__"] = state["__queue__"].pop(0) if state.get("__queue__") else None
    return state 
