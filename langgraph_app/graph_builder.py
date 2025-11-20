from langgraph.graph import StateGraph, END, START
from agentes.decider import nodo_decider
from agentes.agente_resumen import nodo_resumen
from agentes.agente_escritura import nodo_escritura
from agentes.agente_referencias import nodo_referencias
from typing import TypedDict, Optional, List

class GraphState(TypedDict):
    prompt: str
    result: Optional[str]
    __next__: Optional[str]
    __queue__: List[str]



# def build_graph():
#     workflow = StateGraph(GraphState)

#     workflow.add_node("decider", decider_node)
#     workflow.add_node("agente_resumen", agente_resumen_node)
#     workflow.add_node("agente_escritura", agente_escritura_node)
#     workflow.add_node("agente_referencias", agente_referencias_node)
#     print("Nodos agregados al grafo.")

#     workflow.add_edge(START, "decider")
#     workflow.add_conditional_edges(
#         "decider",
#         lambda state: state.get("__next__"),
#         {
#             "agente_resumen": "agente_resumen",
#             "agente_escritura": "agente_escritura",
#             "agente_referencias": "agente_referencias",
#         }
#     )
#     print("Edges condicionales agregados al grafo.")

#     workflow.add_edge("agente_resumen", END)
#     workflow.add_edge("agente_escritura", END)
#     workflow.add_edge("agente_referencias", END)
#     print("Edges finales agregados al grafo.")

#     return workflow.compile()


graph = StateGraph(GraphState)

graph.add_node("decider", nodo_decider)
graph.add_node("resumen", nodo_resumen)
graph.add_node("escritura", nodo_escritura)
graph.add_node("referencias", nodo_referencias)

graph.add_edge(START, "decider")
graph.add_conditional_edges(
    "decider",
    lambda state: state["__next__"],
    {
        "resumen": "resumen",
        "escritura": "escritura",
        "referencias": "referencias",
    }
)

# Cada nodo decide si continúa o termina
for nodo in ["resumen", "escritura", "referencias"]:
    graph.add_conditional_edges(
        nodo,
        lambda state: state["__next__"],
        {
            "resumen": "resumen",
            "escritura": "escritura",
            "referencias": "referencias",
            None: END,
        }
    )

compiled_graph = graph.compile()