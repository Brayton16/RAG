from typing import TypedDict, Optional, List
from langchain_openai import ChatOpenAI

class GraphState(TypedDict):
    prompt: str
    result: Optional[str]
    __next__: Optional[str]
    __queue__: List[str]


def nodo_decider(state: GraphState) -> GraphState:
    prompt_usuario = state.get("prompt", "")


    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.2,
        max_tokens=150,
        top_p=0.95,
    )

    system_msg = (
        "Eres un decider que recibe una consulta escrita por un investigador. "
        "Debes determinar cuál o cuáles de los siguientes agentes deben activarse, en orden, para procesar esa solicitud:"
        "- 'escritura': si se solicita redactar una introducción, sección o texto académico."
        "- 'resumen': si se requiere resumir información."
        "- 'referencias': si se necesitan generar citas o referencias bibliográficas (en formato APA o IEEE)."
        "Responde estrictamente con una lista separada por comas, sin explicaciones, como por ejemplo:"
        "resumen, escritura\n"
        "Si no se puede inferir el propósito, responde con una lista vacía."
    )

    mensaje = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt_usuario}
    ]

    respuesta = llm.invoke(mensaje).content.lower().strip()
    pasos = [x.strip() for x in respuesta.split(",") if x.strip() in ["escritura", "resumen", "referencias"]]

    state["__queue__"] = pasos[1:] if len(pasos) > 1 else []
    state["__next__"] = pasos[0] if pasos else None

    print(f"📌 Nodo DECIDER (LLM) seleccionó: {pasos}")
    return state
