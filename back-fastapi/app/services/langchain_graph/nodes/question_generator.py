"""
Nodo para generar preguntas y descripciones de escenarios.
"""
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

# Configurar el modelo LLM
llm = ChatOpenAI(
    openai_api_key=settings.OPENAI_API_KEY,
    model_name="gpt-4o-mini",
    temperature=0.8
)

def generate_question_and_scenario(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera una pregunta de personalidad y la descripción del escenario
    
    Args:
        data: Diccionario que contiene el tema para la pregunta
        
    Returns:
        Diccionario con la pregunta y descripción del escenario
    """
    theme_value = data.get("theme", "ciencia ficción cósmica")
    
    # Usamos ChatPromptTemplate en lugar de PromptTemplate
    prompt = ChatPromptTemplate.from_template("""
    Genera una pregunta de personalidad de ciencia ficción cósmica sobre {theme}.
    La pregunta debe presentar un dilema o situación difícil donde el usuario debe elegir entre múltiples opciones.
    También genera una descripción detallada del escenario en 3-4 oraciones.
    
    Formato:
    Pregunta: [pregunta]
    Escenario: [descripción detallada]
    """)
    
    # Crear la cadena con LCEL (|) en lugar de LLMChain
    chain = prompt | llm
    
    # Invocar la cadena
    result = chain.invoke({"theme": theme_value})
    
    # Obtener el contenido del mensaje
    content = result.content
    lines = content.strip().split("\n")
    
    question = ""
    scenario = ""
    
    for line in lines:
        if line.startswith("Pregunta:"):
            question = line.replace("Pregunta:", "").strip()
        elif line.startswith("Escenario:"):
            scenario = line.replace("Escenario:", "").strip()
    
    return {
        "question": question,
        "scenario_description": scenario
    }


if __name__ == "__main__":
    print(generate_question_and_scenario({"theme": "ciencia ficción cósmica"}))
