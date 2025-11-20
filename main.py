import os
from langgraph_app.graph_builder import compiled_graph
from vector_storage.pdf_ingestor import ingest_pdf

def ejecutar_asistente(prompt: str, pdf_path: str = None) -> str:
    """
    Ejecuta el asistente multiagente con un prompt y opcionalmente un archivo PDF.

    Args:
        prompt (str): Instrucción o pregunta del usuario.
        pdf_path (str, optional): Ruta al archivo PDF a procesar.

    Returns:
        str: Resultado final generado por los agentes.
    """
    if pdf_path:
        if not os.path.exists(pdf_path) or not pdf_path.endswith(".pdf"):
            return f"❌ El archivo no existe o no es un PDF válido: {pdf_path}"
        
        print(f"📄 Ingestando PDF: {pdf_path}")
        ingest_pdf(pdf_path)
        print("✅ PDF procesado.\n")

    print(f"🧠 Ejecutando agentes con el prompt:\n{prompt}\n")

    inputs = {"prompt": prompt}
    resultado_final = {}

    for output in compiled_graph.stream(inputs):
        for key, value in output.items():
            if key != "intermediate_steps":
                resultado_final = value if isinstance(value, dict) else {"result": value}

    return resultado_final


if __name__ == "__main__":
    user_prompt = input("📝 Ingresa tu prompt: ").strip()
    user_pdf = input("📎 (Opcional) Ruta del PDF: ").strip()
    user_pdf = user_pdf if user_pdf else None

    respuesta = ejecutar_asistente(user_prompt, user_pdf)
    print(respuesta)
