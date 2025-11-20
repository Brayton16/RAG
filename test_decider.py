from decider_llm_flexible import nodo_decider, GraphState

def test_decider(prompt_usuario: str):
    state: GraphState = {
        "prompt": prompt_usuario,
        "result": None,
        "__next__": None,
        "__queue__": []
    }

    state = nodo_decider(state)
    print("➡️ Próximo nodo:", state["__next__"])
    print("📚 Cola de ejecución:", state["__queue__"])
    print("🧠 Prompt original:", state["prompt"])
    print("-" * 50)

# Pruebas
test_decider("Necesito que escribas una introducción académica sobre el impacto de la IA en la educación.")

test_decider("Solo quiero referencias para el artículo attention is all you need de los investigadores de Google.")
test_decider("Hola, necesito que me ayudes el paper attention is all you need de los investigadores de Google ")  # caso sin intención clara
