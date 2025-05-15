"""
Nodo para generar feedback para cada opción.
"""
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI
from app.core.config import settings

# Configurar el modelo LLM
llm = ChatOpenAI(
    openai_api_key=settings.OPENAI_API_KEY,
    model_name="gpt-3.5-turbo",  # Modelo más económico para feedback
    temperature=0.7
)

def generate_feedback(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera feedback personalizado para cada opción
    """
    options = data.get("options", [])
    
    # Usar ChatPromptTemplate en lugar de PromptTemplate
    prompt = ChatPromptTemplate.from_template("""
    Para la respuesta: "{option_text}" (valor: {option_value})
    Con efectos: {effects}
    
    Genera un feedback breve y perspicaz (máximo 15 palabras) que se mostrará al usuario después de elegir esta opción.
    El tono debe ser ligeramente humorístico y cósmico, con un toque filosófico.
    """)
    
    # Crear la cadena con LCEL (|) en lugar de LLMChain
    chain = prompt | llm
    
    options_with_feedback = []
    
    for option in options:
        try:
            # Invocar la cadena
            result = chain.invoke({
                "option_text": option["text"], 
                "option_value": option["value"],
                "effects": str(option["effect"])
            })
            
            # Obtener el contenido del mensaje
            feedback = result.content.strip()
            
            # Limitar longitud del feedback
            if len(feedback.split()) > 15:
                feedback = " ".join(feedback.split()[:15])
            
            option_with_feedback = option.copy()
            option_with_feedback["feedback"] = feedback
            options_with_feedback.append(option_with_feedback)
            
        except Exception as e:
            print(f"Error generating feedback: {str(e)}")
            # Si hay error, usar feedback genérico
            option_with_feedback = option.copy()
            option_with_feedback["feedback"] = "Una elección interesante para un viajero cósmico."
            options_with_feedback.append(option_with_feedback)
    
    return {"options_with_feedback": options_with_feedback}
