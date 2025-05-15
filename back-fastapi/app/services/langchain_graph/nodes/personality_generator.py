from langgraph.graph import Graph
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

def build_personality_question_graph():
    """Construye el grafo de generación de preguntas de personalidad"""
    graph = Graph()
    
    # Añadir nodos
    graph.add_node("generate_question", generate_question_and_scenario)
    graph.add_node("generate_image", generate_image_node)
    graph.add_node("generate_options", generate_options)
    graph.add_node("generate_feedback", generate_feedback)
    
    # Definir el flujo
    graph.add_edge("generate_question", "generate_image")
    graph.add_edge("generate_image", "generate_options")
    graph.add_edge("generate_options", "generate_feedback")
    
    return graph
