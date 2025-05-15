# nodes/options_generator.py
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings
import re

# Configurar el modelo LLM
llm = ChatOpenAI(
    openai_api_key=settings.OPENAI_API_KEY,
    model_name="gpt-4o-mini",  # Cambiado a gpt-4o-mini por consistencia
    temperature=0.7
)

def generate_options(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera 4 opciones de respuesta con emojis y efectos
    """
    question = data.get("question", "")
    scenario = data.get("scenario_description", "")
    
    # Usar ChatPromptTemplate en lugar de PromptTemplate
    prompt = ChatPromptTemplate.from_template("""
    Para la pregunta: {question}
    En el escenario: {scenario}
    
    Genera exactamente 4 posibles respuestas ordenadas desde la más valiente/arriesgada (4) 
    hasta la más cautelosa/conservadora (1).
    
    Para cada respuesta incluye:
    1. Texto de la respuesta (1 frase)
    2. Un emoji apropiado
    3. Valor numérico (4=más arriesgada, 1=más conservadora)
    4. Efectos en las estadísticas de personalidad:
       - quantum_charisma (0-15)
       - absurdity_resistance (0-15)
       - sarcasm_level (0-15)
       - time_warping (0-18)
       - cosmic_luck (0-10)
       Cada opción debe afectar 2-3 estadísticas distintas.
    
    Formato para cada opción:
    Opción [valor]: [texto] | Emoji: [emoji] | Efectos: quantum_charisma=[valor], absurdity_resistance=[valor], etc.
    """)
    
    # Crear la cadena con LCEL (|) en lugar de LLMChain
    chain = prompt | llm
    
    # Invocar la cadena
    result = chain.invoke({"question": question, "scenario": scenario})
    
    # Obtener el contenido del mensaje
    content = result.content
    lines = [line for line in content.strip().split("\n") if line.startswith("Opción")]
    
    options = []
    for line in lines:
        try:
            # Parsear cada línea
            parts = line.split("|")
            
            option_part = parts[0].strip()
            emoji_part = parts[1].strip() if len(parts) > 1 else "Emoji: ❓"
            effects_part = parts[2].strip() if len(parts) > 2 else "Efectos: quantum_charisma=5, absurdity_resistance=5"
            
            # Método flexible para extraer el valor numérico (1-4)
            # Primero intentamos encontrar el valor entre corchetes si existe
            bracket_match = re.search(r'Opción\s*\[(\d+)\]', option_part)
            if bracket_match:
                value = int(bracket_match.group(1))
            else:
                # Si no hay corchetes, buscamos el primer número después de "Opción"
                number_match = re.search(r'Opción\s*(\d+)', option_part)
                if number_match:
                    value = int(number_match.group(1))
                else:
                    # Si no podemos encontrar un número, asignamos un valor por defecto
                    value = 1
                    print(f"No se pudo encontrar un valor numérico en: {option_part}, asignando valor por defecto: 1")
            
            # Extraer el texto de manera más flexible
            # Si tenemos corchetes, buscamos después del cierre "]:"
            if bracket_match:
                text_start = option_part.find("]:") + 2
                text = option_part[text_start:].strip()
            else:
                # De lo contrario, buscamos después de "Opción X:"
                text_start = option_part.find(":")
                if text_start != -1:
                    text = option_part[text_start + 1:].strip()
                else:
                    # Si todo falla, usamos toda la parte como texto
                    text = option_part
                    print(f"Usando todo el texto como contenido: {text}")
            
            # Extraer el emoji de manera más flexible
            emoji_parts = emoji_part.split(":")
            if len(emoji_parts) > 1:
                emoji = emoji_parts[1].strip()
            else:
                emoji = "❓"
                print(f"No se pudo extraer emoji de: {emoji_part}, usando emoji por defecto")
            
            # Parsear efectos de manera más flexible
            effects = {}
            effects_str = ""
            
            if ":" in effects_part:
                effects_str = effects_part.split(":", 1)[1].strip()
            else:
                effects_str = effects_part.strip()
            
            # Procesar cada efecto individualmente
            for effect_pair in re.finditer(r'(\w+)\s*=\s*(\d+)', effects_str):
                key, val = effect_pair.groups()
                effects[key.strip()] = int(val.strip())
            
            # Asegurarnos de que tenemos al menos un efecto
            if not effects:
                effects = {"quantum_charisma": 5, "absurdity_resistance": 5}
                print(f"No se pudieron extraer efectos de: {effects_part}, usando efectos por defecto")
            
            options.append({
                "text": text,
                "emoji": emoji,
                "value": value,
                "effect": effects
            })
        except Exception as e:
            print(f"Error parsing option: {line}, Error: {str(e)}")
            # Continuar con la siguiente opción
    
    # Asegurar que tenemos exactamente 4 opciones ordenadas por valor
    options = sorted(options, key=lambda x: x["value"], reverse=True)
    
    # Limitar a 4 opciones
    while len(options) > 4:
        options.pop()
    
    # Si tenemos menos de 4, rellenar con opciones genéricas
    while len(options) < 4:
        missing_value = 4 - len(options)
        options.append({
            "text": f"Opción genérica {missing_value}",
            "emoji": "❓",
            "value": missing_value,
            "effect": {
                "quantum_charisma": 5,
                "absurdity_resistance": 5
            }
        })
    
    return {"options": options}

if __name__ == "__main__":
    print(generate_options({"question": "¿Qué harías?", "scenario": "Estás en una isla desierta y tienes que elegir entre dos opciones: 1. Construir una casa o 2. Cazar animales para comer."}))