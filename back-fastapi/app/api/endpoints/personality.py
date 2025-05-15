from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Any, List, Dict
import json
import os


from app.api.schemas.personality import (
    PersonalityQuestion, PersonalityTestSubmit, 
    PersonalityTestResults, PersonalityStats
)
from app.api.dependencies.auth import get_current_active_user
from app.api.schemas.user import User
from app.db.session import get_db
from app.db.repositories.personality import personality_repository
from app.core.config import settings
import asyncio
from datetime import datetime
from uuid import uuid4

# Importar funciones del generador simple
from app.services.simple_generator import generate_personality_question, generate_fallback_question

router = APIRouter()


@router.get("/questions", response_model=List[PersonalityQuestion])

async def get_personality_questions(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 4,
    lang: str = "en",
    background_tasks: BackgroundTasks
) -> Any:
    """
    Obtiene las preguntas para el test de personalidad.
    Este endpoint es público y no requiere autenticación.
    Siempre devuelve exactamente 4 preguntas.
    
    Si GENERATE_QUESTIONS_ON_DEMAND está habilitado, genera preguntas dinámicamente.
    Si está deshabilitado, devuelve preguntas de fallback.
    
    Soporta idiomas inglés (en) y español (es) a través del parámetro lang.
    """
    print(f"Generando preguntas de personalidad en idioma: {lang}")
    # Verificar si debemos generar preguntas on-demand
    generate_on_demand = os.getenv('GENERATE_QUESTIONS_ON_DEMAND', 'false').lower() == 'true'
    print(f"GENERATE_QUESTIONS_ON_DEMAND: {generate_on_demand}")
    # Crear una lista para almacenar las preguntas de respuesta
    final_questions = []
    
    if generate_on_demand:
        try:
            # Definir temas para las preguntas
            themes = [
                "viaje espacial", 
                "encuentro alienígena", 
                "paradoja temporal",
                "colonización espacial"
            ]
            
            # Importar el generador simple
            try:
                print("Importando generador simple...")
                from app.services.simple_generator import generate_personality_question
                
                # Generar preguntas para cada tema
                for i in range(min(limit, len(themes))):
                    try:
                        print(f"Generando pregunta para tema: {themes[i]}")
                        question_data = await generate_personality_question(themes[i], lang)
                        
                        # Crear objeto de pregunta
                        question = {
                            "id": str(uuid4()),
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat(),
                            "question": question_data["question"],
                            "options": question_data["options"],
                            "context_image": question_data["context_image"],
                            "scenario_description": question_data["scenario_description"]
                        }
                        
                        final_questions.append(question)
                    except Exception as e:
                        print(f"Error generando pregunta para tema {themes[i]}: {str(e)}")
                
                # Si hemos generado preguntas, convertir y devolver
                if final_questions:
                    print(f"Generadas {len(final_questions)} preguntas con éxito")
                    return [PersonalityQuestion(**q) for q in final_questions]
                
            except Exception as e:
                print(f"Error importando generador simple: {str(e)}")
                # Continuar con fallback
        
        except Exception as e:
            print(f"Error en proceso de generación: {str(e)}")
            # Continuar con fallback
    
    # Si estamos aquí, usamos fallback
    print("Usando preguntas fallback...")
    themes = ["viaje espacial", "encuentro alienígena", "paradoja temporal", "colonización espacial"]
    
    for i, theme in enumerate(themes[:limit]):
        try:
            # Intentar usar el generador fallback pero con idioma seleccionado
            print(f"Generando pregunta fallback para tema: {theme}, idioma: {lang}")
            fallback_question = generate_fallback_question(theme, lang)
            question = PersonalityQuestion(
                id=uuid4(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                question=fallback_question["question"],
                scenario_description=fallback_question["scenario_description"],
                context_image=fallback_question["context_image"],
                options=fallback_question["options"]
            )
        except Exception as e:
            print(f"Error al generar pregunta fallback: {e}")
            # Fallback muy básico si todo lo demás falla
            options = [
                {
                    "text": f"Opción fallback 1 para {theme}" if lang == "es" else f"Fallback option 1 for {theme}", 
                    "emoji": "🚀", 
                    "value": 4, 
                    "effect": {"quantum_charisma": 10},
                    "feedback": f"Feedback fallback 1 para {theme}" if lang == "es" else f"Fallback feedback 1 for {theme}"
                },
                {
                    "text": f"Opción fallback 2 para {theme}" if lang == "es" else f"Fallback option 2 for {theme}", 
                    "emoji": "🔭", 
                    "value": 3, 
                    "effect": {"absurdity_resistance": 8},
                    "feedback": f"Feedback fallback 2 para {theme}" if lang == "es" else f"Fallback feedback 2 for {theme}"
                },
                {
                    "text": f"Opción fallback 3 para {theme}" if lang == "es" else f"Fallback option 3 for {theme}", 
                    "emoji": "🌌", 
                    "value": 2, 
                    "effect": {"time_warping": 12},
                    "feedback": f"Feedback fallback 3 para {theme}" if lang == "es" else f"Fallback feedback 3 for {theme}"
                },
                {
                    "text": f"Opción fallback 4 para {theme}" if lang == "es" else f"Fallback option 4 for {theme}", 
                    "emoji": "🛰️", 
                    "value": 1, 
                    "effect": {"cosmic_luck": 5},
                    "feedback": f"Feedback fallback 4 para {theme}" if lang == "es" else f"Fallback feedback 4 for {theme}"
                }
            ]
            
            question = PersonalityQuestion(
                id=uuid4(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                question=f"Pregunta fallback sobre {theme}" if lang == "es" else f"Fallback question about {theme}",
                scenario_description=f"Descripción fallback de escenario sobre {theme}" if lang == "es" else f"Fallback scenario description about {theme}",
                context_image="/static/images/fallback/cosmic_default.webp",
                options=options
            )
        
        final_questions.append(question)
    
    return final_questions


@router.post("/results", response_model=PersonalityTestResults)
async def submit_personality_test(
    *,
    db: Session = Depends(get_db),
    test_results: PersonalityTestSubmit,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Envía las respuestas del test de personalidad y obtiene los resultados.
    """
    # Verificar que el usuario que envía las respuestas es el mismo que el del token
    if str(test_results.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de usuario en los resultados no coincide con el usuario autenticado",
        )
    
    # Calcular estadísticas basadas en las respuestas
    stats_data = personality_repository.calculate_personality_stats(
        answers=test_results.answers
    )
    
    # Crear y devolver el objeto de resultados
    stats = PersonalityStats(
        quantum_charisma=stats_data["quantum_charisma"],
        absurdity_resistance=stats_data["absurdity_resistance"],
        sarcasm_level=stats_data["sarcasm_level"],
        time_warping=stats_data["time_warping"],
        cosmic_luck=stats_data["cosmic_luck"],
    )
    
    results = PersonalityTestResults(stats=stats)
    
    return results 