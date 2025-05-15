#!/usr/bin/env python
"""
Script para inicializar la base de datos con los datos actualizados.
"""

import logging
from sqlalchemy.orm import Session

from app.db.session import Base, engine, SessionLocal
from app.db.models import *  # Importar todos los modelos
from app.api.schemas.personality import PersonalityQuestionCreate, PersonalityOptionBase
from app.db.repositories.personality import personality_repository

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Inicializa la base de datos con datos de ejemplo.
    """
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Limpiar datos existentes
        db.query(PersonalityQuestion).delete()
        db.commit()
        
        logger.info("Creando datos iniciales...")
        
        # Crear exactamente 4 preguntas de personalidad
        questions = [
            PersonalityQuestionCreate(
                question="Si te encuentras un agujero de gusano en tu armario, ¿qué harías?",
                context_image="https://example.com/images/wormhole_closet.jpg",
                scenario_description="Tras un largo día en la Estación Espacial Zeta-9, regresas a tu camarote para descansar. Al abrir tu armario para guardar tu uniforme, descubres un brillante vórtice azulado que parece distorsionar el espacio-tiempo. Los escáneres indican que es un agujero de gusano estable, pero su destino es desconocido.",
                options=[
                    PersonalityOptionBase(
                        text="Lo atravieso sin pensarlo dos veces",
                        emoji="🚀",
                        value=4,
                        effect={"quantum_charisma": 10, "time_warping": 15},
                        feedback="¡Aventurero cósmico en potencia!"
                    ),
                    PersonalityOptionBase(
                        text="Lo estudio primero con una cámara",
                        emoji="🔍",
                        value=3,
                        effect={"absurdity_resistance": 8, "cosmic_luck": 5},
                        feedback="Cautela científica, pero curiosidad cósmica"
                    ),
                    PersonalityOptionBase(
                        text="Lo ignoro, seguro es una alucinación",
                        emoji="🙄",
                        value=2,
                        effect={"sarcasm_level": 12, "absurdity_resistance": 15},
                        feedback="La negación es la primera fase del encuentro cósmico"
                    ),
                    PersonalityOptionBase(
                        text="Llamo a un compañero para que lo verifique",
                        emoji="👥",
                        value=1,
                        effect={"quantum_charisma": 5, "absurdity_resistance": 5, "cosmic_luck": 3},
                        feedback="Buscar testigos es racional, pero los fenómenos cuánticos suelen ser tímidos"
                    )
                ]
            ),
            PersonalityQuestionCreate(
                question="Un alien te ofrece la respuesta a cualquier pregunta. ¿Qué le preguntas?",
                context_image="https://example.com/images/alien_encounter.jpg",
                scenario_description="Durante tu turno de guardia en el Observatorio Lunar, una luz brillante inunda la sala de control. Cuando tus ojos se adaptan, ves a un ser de luz translúcida frente a ti. Telepáticamente, te comunica que es un Guardián del Conocimiento Universal y puede responder exactamente una pregunta tuya con total verdad y precisión. 'Elige sabiamente', te dice, 'pues esta oportunidad solo ocurre una vez en la vida de una especie'.",
                options=[
                    PersonalityOptionBase(
                        text="¿Cuál es el significado de la vida?",
                        emoji="🌌",
                        value=4,
                        effect={"quantum_charisma": 5, "cosmic_luck": 10},
                        feedback="Pregunta clásica, respuesta probablemente decepcionante"
                    ),
                    PersonalityOptionBase(
                        text="¿Tienen memes en su planeta?",
                        emoji="😂",
                        value=3,
                        effect={"sarcasm_level": 20, "absurdity_resistance": 8},
                        feedback="Prioridades correctas, ¡la cultura es importante!"
                    ),
                    PersonalityOptionBase(
                        text="¿Cómo viajan más rápido que la luz?",
                        emoji="💫",
                        value=2,
                        effect={"time_warping": 15, "quantum_charisma": 5},
                        feedback="Conocimiento práctico, pero ¿podrías entender la respuesta?"
                    ),
                    PersonalityOptionBase(
                        text="¿Por qué has elegido contactar conmigo?",
                        emoji="🤔",
                        value=1,
                        effect={"quantum_charisma": 8, "absurdity_resistance": 5, "cosmic_luck": 5},
                        feedback="Intrigante. A veces conocer el 'por qué' es más valioso que el 'cómo'"
                    )
                ]
            ),
            PersonalityQuestionCreate(
                question="Descubres una máquina del tiempo abandonada. ¿Qué haces?",
                context_image="https://example.com/images/time_machine.jpg",
                scenario_description="Durante una expedición científica en las ruinas de una antigua civilización alienígena, tu equipo descubre una extraña estructura circular con paneles de control cristalinos. Después de semanas de estudio, determinan que es una especie de dispositivo de manipulación temporal, milagrosamente intacto. Los análisis preliminares sugieren que podría permitir viajes precisos a través del tiempo, pero nadie sabe exactamente cómo funciona o qué riesgos conlleva su uso.",
                options=[
                    PersonalityOptionBase(
                        text="Viajar al pasado para presenciar eventos históricos",
                        emoji="⏪",
                        value=4,
                        effect={"quantum_charisma": 0, "time_warping": 18, "cosmic_luck": 6},
                        feedback="La tentación de ser testigo de la historia es comprensible, pero recuerda: observa, no interfieras"
                    ),
                    PersonalityOptionBase(
                        text="Viajar al futuro para ver la evolución de la humanidad",
                        emoji="⏩",
                        value=3,
                        effect={"quantum_charisma": 5, "time_warping": 15, "cosmic_luck": 5},
                        feedback="La curiosidad por nuestro destino es natural, pero ¿estás preparado para lo que podrías descubrir?"
                    ),
                    PersonalityOptionBase(
                        text="Estudiarla sin activarla para entender la tecnología",
                        emoji="🔬",
                        value=2,
                        effect={"absurdity_resistance": 12, "time_warping": 5},
                        feedback="Decisión prudente. El conocimiento antes que la acción puede evitar paradojas temporales"
                    ),
                    PersonalityOptionBase(
                        text="Sellarla para que nadie pueda usarla jamás",
                        emoji="🔒",
                        value=1,
                        effect={"absurdity_resistance": 15, "sarcasm_level": 5},
                        feedback="Cauteloso. Pero recuerda que lo que se sella una vez, a menudo se redescubre"
                    )
                ]
            ),
            PersonalityQuestionCreate(
                question="Te ofrecen unirte a una misión para colonizar un planeta desconocido. ¿Qué decides?",
                context_image="https://example.com/images/colony_ship.jpg",
                scenario_description="La Agencia Espacial Intergaláctica ha descubierto un planeta potencialmente habitable a 20 años luz de la Tierra. Han desarrollado una nave con tecnología de hibernación para un viaje de 25 años. Están reclutando especialistas de diversas áreas, y tu perfil ha sido seleccionado. La misión es de alto riesgo pero podría cambiar el futuro de la humanidad. No hay garantía de regreso.",
                options=[
                    PersonalityOptionBase(
                        text="Me uno inmediatamente, la aventura de una vida",
                        emoji="🌠",
                        value=4,
                        effect={"quantum_charisma": 12, "cosmic_luck": 8},
                        feedback="El espíritu pionero es lo que impulsa a la humanidad hacia las estrellas"
                    ),
                    PersonalityOptionBase(
                        text="Negocio condiciones especiales antes de aceptar",
                        emoji="🤝",
                        value=3,
                        effect={"quantum_charisma": 8, "absurdity_resistance": 7, "sarcasm_level": 5},
                        feedback="Prudente pero ambicioso, la marca de un explorador calculador"
                    ),
                    PersonalityOptionBase(
                        text="Pido un puesto en el equipo de tierra para apoyar remotamente",
                        emoji="📡",
                        value=2,
                        effect={"absurdity_resistance": 10, "time_warping": 5, "cosmic_luck": 5},
                        feedback="El soporte es tan importante como la acción directa"
                    ),
                    PersonalityOptionBase(
                        text="Rechazo la oferta, prefiero seguir con mi vida en la Tierra",
                        emoji="🌍",
                        value=1,
                        effect={"absurdity_resistance": 15, "sarcasm_level": 10},
                        feedback="No todas las aventuras requieren abandonar el hogar"
                    )
                ]
            )
        ]
        
        for question_data in questions:
            question = personality_repository.create(db=db, obj_in=question_data)
            logger.info(f"Pregunta de personalidad creada: {question.question[:30]}...")
        
        logger.info("Inicialización de la base de datos completada.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 