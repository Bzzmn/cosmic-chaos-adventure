import os
import asyncio
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

async def generate_question(theme):
    """Generate a personality question using OpenAI API directly"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un generador de preguntas de personalidad para un juego de ciencia ficción cósmica."},
                {"role": "user", "content": f"""
                Genera una pregunta de personalidad de ciencia ficción cósmica sobre {theme}.
                La pregunta debe presentar un dilema o situación difícil donde el usuario debe elegir entre múltiples opciones.
                También genera una descripción detallada del escenario en 3-4 oraciones.
                
                Formato:
                Pregunta: [pregunta]
                Escenario: [descripción detallada]
                """}
            ],
            temperature=0.8
        )
        
        # Extract content from response
        content = response.choices[0].message.content
        return content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return None

async def generate_options(question, scenario):
    """Generate options for the question using OpenAI API directly"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un generador de opciones para preguntas de personalidad en un juego de ciencia ficción cósmica."},
                {"role": "user", "content": f"""
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
                """}
            ],
            temperature=0.7
        )
        
        # Extract content from response
        content = response.choices[0].message.content
        return content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return None

async def generate_feedback(options_text):
    """Generate feedback for options using OpenAI API directly"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un generador de feedback para opciones de preguntas de personalidad en un juego de ciencia ficción cósmica."},
                {"role": "user", "content": f"""
                Para cada una de estas opciones, genera un feedback breve y perspicaz (máximo 15 palabras)
                que se mostrará al usuario después de elegir esta opción.
                El tono debe ser ligeramente humorístico y cósmico, con un toque filosófico.
                
                Las opciones son:
                {options_text}
                
                Formato para cada feedback:
                Opción [valor]: Feedback: [texto del feedback]
                """}
            ],
            temperature=0.7
        )
        
        # Extract content from response
        content = response.choices[0].message.content
        return content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return None

def parse_options(options_text, feedback_text):
    """Parse options and feedback from text responses"""
    options = []
    
    # Parse options
    lines = [line for line in options_text.strip().split("\n") if line.startswith("Opción")]
    
    for line in lines:
        try:
            # Parse each line
            parts = line.split("|")
            
            option_part = parts[0].strip()
            emoji_part = parts[1].strip()
            effects_part = parts[2].strip()
            
            # Extract the value
            value_start = option_part.find("[") + 1
            value_end = option_part.find("]")
            value = int(option_part[value_start:value_end])
            
            # Extract the text
            text = option_part[option_part.find(":") + 1:].strip()
            
            # Extract the emoji
            emoji = emoji_part.split(":")[1].strip()
            
            # Parse effects
            effects_str = effects_part.split(":")[1].strip()
            effects = {}
            
            for effect in effects_str.split(","):
                effect = effect.strip()
                key, val = effect.split("=")
                effects[key.strip()] = int(val.strip())
            
            options.append({
                "text": text,
                "emoji": emoji,
                "value": value,
                "effect": effects
            })
        except Exception as e:
            print(f"Error parsing option: {line}, Error: {str(e)}")
    
    # Add feedback to options
    feedback_lines = [line for line in feedback_text.strip().split("\n") if line.startswith("Opción")]
    
    for feedback_line in feedback_lines:
        try:
            # Parse value and feedback
            value_start = feedback_line.find("[") + 1
            value_end = feedback_line.find("]")
            value = int(feedback_line[value_start:value_end])
            
            feedback = feedback_line.split("Feedback:")[1].strip()
            
            # Find matching option and add feedback
            for option in options:
                if option["value"] == value:
                    option["feedback"] = feedback
                    break
        except Exception as e:
            print(f"Error parsing feedback: {feedback_line}, Error: {str(e)}")
    
    return options

async def test_llm_generation():
    """Test the LLM-based generation of personality questions and images"""
    print("🚀 Starting LLM generation test...")
    
    # Generate a personality question with the theme "paradoja temporal"
    theme = "paradoja temporal"
    print(f"Generating question with theme: {theme}")
    
    try:
        # Generate question and scenario
        question_response = await generate_question(theme)
        if not question_response:
            raise Exception("Failed to generate question and scenario")
            
        print("\nQuestion and scenario generated:")
        print(question_response)
        
        # Parse question and scenario
        lines = question_response.strip().split("\n")
        question = ""
        scenario = ""
        
        for line in lines:
            if line.startswith("Pregunta:"):
                question = line.replace("Pregunta:", "").strip()
            elif line.startswith("Escenario:"):
                scenario = line.replace("Escenario:", "").strip()
        
        if not question or not scenario:
            print("Warning: Could not parse question or scenario correctly.")
            # Try to infer from the format
            if len(lines) >= 2:
                question = lines[0].replace("Pregunta:", "").strip()
                scenario = lines[1].replace("Escenario:", "").strip()
        
        # Generate options
        print("\nGenerating options...")
        options_response = await generate_options(question, scenario)
        if not options_response:
            raise Exception("Failed to generate options")
        print(options_response)
        
        # Generate feedback
        print("\nGenerating feedback...")
        feedback_response = await generate_feedback(options_response)
        if not feedback_response:
            raise Exception("Failed to generate feedback")
        print(feedback_response)
        
        # Parse options and feedback
        options = parse_options(options_response, feedback_response)
        
        if not options:
            # Use fallback options if parsing failed
            options = [
                {"text": "Opción simulada 1", "emoji": "🚀", "value": 4, "effect": {"quantum_charisma": 10}, "feedback": "Feedback para opción 1"},
                {"text": "Opción simulada 2", "emoji": "🔭", "value": 3, "effect": {"absurdity_resistance": 8}, "feedback": "Feedback para opción 2"},
                {"text": "Opción simulada 3", "emoji": "🌌", "value": 2, "effect": {"time_warping": 12}, "feedback": "Feedback para opción 3"},
                {"text": "Opción simulada 4", "emoji": "🛰️", "value": 1, "effect": {"cosmic_luck": 5}, "feedback": "Feedback para opción 4"}
            ]
        
        # Create result object
        result = {
            "question": question,
            "scenario_description": scenario,
            "context_image": "/static/images/fallback/cosmic_default.jpg",
            "options": options
        }
        
        # Print the result in a formatted way
        print("\n✅ Generation successful!")
        print(f"Question: {result['question']}")
        print(f"Scenario: {result['scenario_description']}")
        print(f"Image URL: {result['context_image']}")
        print("\nOptions:")
        for option in result['options']:
            print(f"  - {option['emoji']} {option['text']} (value: {option['value']})")
            print(f"    Effect: {option['effect']}")
            print(f"    Feedback: {option.get('feedback', 'No feedback')}")
            print()
        
        # Save the result to a JSON file for reference
        with open("generated_question.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("Result saved to generated_question.json")
            
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_llm_generation()) 