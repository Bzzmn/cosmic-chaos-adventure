
from langgraph.graph import StateGraph, START, END
from typing import Dict, Any, List, TypedDict
import asyncio


# Importaciones de los nodos
from app.services.langchain_graph.nodes.question_generator import generate_question_and_scenario
from app.services.langchain_graph.nodes.image_generator import GeminiImageGenerator
from app.services.langchain_graph.nodes.options_generator import generate_options
from app.services.langchain_graph.nodes.feedback_generator import generate_feedback

# Inicializar generador de imágenes
image_generator = GeminiImageGenerator()

async def generate_image_node(data: dict) -> dict:
    """Nodo del grafo para generación de imágenes"""
    scenario_description = data.get("scenario_description", "")
    image_result = await image_generator.generate_image(scenario_description)
    return image_result

class State(TypedDict):
    question: str
    scenario_description: str
    context_image: str
    options: List[Dict[str, Any]]

def build_personality_question_graph():
    """Construye el grafo de generación de preguntas de personalidad"""
    graph = StateGraph(State)
    # Añadir nodos
    graph.add_node("generate_question", generate_question_and_scenario)
    # graph.add_node("generate_image", generate_image_node)
    # graph.add_node("generate_options", generate_options)
    # graph.add_node("generate_feedback", generate_feedback)
    
    # Definir el flujo
    graph.add_edge(START, "generate_question")
    graph.add_edge("generate_question", END)
    # graph.add_edge("generate_question", "generate_image")
    # graph.add_edge("generate_image", "generate_options")
    # graph.add_edge("generate_options", "generate_feedback")
    
    # Envolver en AsyncGraph para soporte asincrónico
    from app.services.langchain_graph.async_wrapper import AsyncGraph
    return AsyncGraph(graph)

async def generate_personality_question(theme: str) -> Dict[str, Any]:
    """
    Genera una pregunta de personalidad completa basada en un tema
    
    Args:
        theme: Tema para la pregunta (ej: "viaje espacial", "encuentro alienígena")
        
    Returns:
        Dict con la estructura completa de PersonalityQuestion
    """
    graph = build_personality_question_graph()

    print(f"Graph: {graph}")
    
    if graph is None:
        # Fallback si langgraph no está disponible
        return generate_fallback_question(theme)
    
    try:
        # Ejecutar el grafo - Ahora usamos invoke, que es el método correcto en langgraph 0.4.3
        result = await graph.arun({"theme": theme})
        
        # Estructurar el resultado final
        personality_question = {
            "question": result["generate_question"]["question"],
            "context_image": result["generate_image"]["context_image"],
            "scenario_description": result["generate_question"]["scenario_description"],
            "options": result["generate_feedback"]["options_with_feedback"]
        }
        
        return personality_question
    except Exception as e:
        print(f"Error en grafo de generación de preguntas: {str(e)}")
        # Si hay cualquier error en la ejecución del grafo, usar fallback
        return generate_fallback_question(theme)

def generate_fallback_question(theme: str) -> Dict[str, Any]:
    """
    Genera una pregunta de fallback cuando langgraph no está disponible o falla
    
    Args:
        theme: Tema para la pregunta
        
    Returns:
        Dict con estructura de PersonalityQuestion
    """
    return {
        "question": f"Pregunta fallback sobre {theme}",
        "context_image": "/static/images/fallback/cosmic_default.jpg",
        "scenario_description": f"Descripción fallback de escenario sobre {theme}.",
        "options": [
            {"text": f"Opción fallback 1 para {theme}", "emoji": "🚀", "value": 4, "effect": {"quantum_charisma": 10}, "feedback": f"Feedback fallback 1 para {theme}"},
            {"text": f"Opción fallback 2 para {theme}", "emoji": "🔭", "value": 3, "effect": {"absurdity_resistance": 8}, "feedback": f"Feedback fallback 2 para {theme}"},
            {"text": f"Opción fallback 3 para {theme}", "emoji": "🌌", "value": 2, "effect": {"time_warping": 12}, "feedback": f"Feedback fallback 3 para {theme}"},
            {"text": f"Opción fallback 4 para {theme}", "emoji": "🛰️", "value": 1, "effect": {"cosmic_luck": 5}, "feedback": f"Feedback fallback 4 para {theme}"}
        ]
    }

async def generate_background_questions(db, num_questions):
    """
    Función para generar preguntas en background
    Mantener para compatibilidad pero no almacenar en DB
    """
    themes = [
        "viaje espacial", 
        "encuentro alienígena", 
        "paradoja temporal",
        "colonización espacial"
    ]
    
    for i in range(num_questions):
        theme_idx = i % len(themes)
        
        try:
            await generate_personality_question(themes[theme_idx])
            print(f"Pregunta generada exitosamente para tema: {themes[theme_idx]}")
        except Exception as e:
            print(f"Error generando pregunta para tema {themes[theme_idx]}: {str(e)}")

if __name__ == "__main__":
    print("Generando preguntas en background...")
    asyncio.run(generate_background_questions(None, 4))


