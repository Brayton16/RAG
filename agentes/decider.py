from typing import TypedDict, Optional, List

class GraphState(TypedDict):
    prompt: str
    result: Optional[str]
    __next__: Optional[str]
    __queue__: List[str]

def nodo_decider(state: GraphState) -> GraphState:
    prompt = state.get("prompt", "").lower()
    pasos = []

    if "resumen" in prompt or "resumir" in prompt:
        pasos.append("resumen")
    if "introduccion" in prompt or "redacta" in prompt or "escribe" in prompt:
        pasos.append("escritura")
    if "referencias" in prompt or "citas" in prompt:
        pasos.append("referencias")

    state["__queue__"] = pasos[1:] if len(pasos) > 1 else []
    state["__next__"] = pasos[0] if pasos else None

    print(f"📌 Nodo DECIDER seleccionó: {pasos}")
    return state