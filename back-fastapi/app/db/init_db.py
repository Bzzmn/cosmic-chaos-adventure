"""
Script para inicializar la base de datos con datos de ejemplo.
"""

import logging
from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.db.models import *  # Importar todos los modelos
from app.core.config import settings

# Importar repositorios
from app.db.repositories.user import user_repository
from app.db.repositories.character import character_repository
from app.db.repositories.artifact import artifact_repository
from app.db.repositories.adventure import adventure_repository
from app.db.repositories.personality import personality_repository

# Importar esquemas
from app.api.schemas.user import UserCreate
from app.api.schemas.artifact import ArtifactCreate
from app.api.schemas.personality import PersonalityQuestionCreate, PersonalityOptionBase
from app.api.schemas.adventure import AdventureCreate

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """
    Inicializa la base de datos con datos de ejemplo.
    
    Args:
        db: Sesión de base de datos.
    """
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Verificar si ya hay datos
    user = db.query(User).first()
    if user:
        logger.info("La base de datos ya contiene datos. Saltando inicialización.")
        return
    
    logger.info("Creando datos iniciales...")
    
    # Crear usuario de prueba
    admin_user = UserCreate(
        name="Admin User",
        email="admin@example.com",
        password="password123"
    )
    user = user_repository.create(db=db, obj_in=admin_user)
    logger.info(f"Usuario creado con ID: {user.id}")
    
    # Crear artefactos de ejemplo
    artifacts = [
        ArtifactCreate(
            name="Amplificador de Carisma Cuántico",
            description="Aumenta temporalmente tu carisma cuántico en situaciones sociales cósmicas.",
            image_url="https://example.com/artifacts/quantum_charisma.png",
            effect={
                "stat": "quantum_charisma",
                "bonus": 15,
                "duration": 3
            }
        ),
        ArtifactCreate(
            name="Escudo de Absurdidad",
            description="Te protege contra los niveles más altos de absurdidad cósmica.",
            image_url="https://example.com/artifacts/absurdity_shield.png",
            effect={
                "stat": "absurdity_resistance",
                "bonus": 20,
                "duration": 2
            }
        ),
        ArtifactCreate(
            name="Intensificador de Sarcasmo",
            description="Potencia tus comentarios sarcásticos a niveles interdimensionales.",
            image_url="https://example.com/artifacts/sarcasm_enhancer.png",
            effect={
                "stat": "sarcasm_level",
                "bonus": 25,
                "duration": None
            }
        )
    ]
    
    for artifact_data in artifacts:
        artifact = artifact_repository.create(db=db, obj_in=artifact_data)
        logger.info(f"Artefacto creado: {artifact.name}")
    
    # Crear preguntas de personalidad
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
        )
    ]
    
    for question_data in questions:
        question = personality_repository.create(db=db, obj_in=question_data)
        logger.info(f"Pregunta de personalidad creada: {question.question[:30]}...")
    
    # Crear una aventura de ejemplo
    adventure_data = AdventureCreate(
        title="La Anomalía Temporal",
        steps=[
            {
                "narrative": "Te despiertas en una nave espacial desconocida. Las luces parpadean y hay una sensación extraña en el aire.",
                "options": [
                    {
                        "text": "Explorar la nave",
                        "outcome": "Encuentras una sala de control con extraños símbolos.",
                        "next_step": 1,
                        "artifact_id": None
                    },
                    {
                        "text": "Volver a dormir",
                        "outcome": "Sueñas con estrellas que hablan. Te despiertas sobresaltado.",
                        "next_step": 2,
                        "artifact_id": None
                    }
                ]
            },
            {
                "narrative": "La sala de control tiene pantallas con símbolos alienígenas. Hay un objeto brillante sobre el panel.",
                "options": [
                    {
                        "text": "Tocar el objeto brillante",
                        "outcome": "¡Es un artefacto! Absorbes su poder.",
                        "next_step": 3,
                        "artifact_id": "some-artifact-id"
                    },
                    {
                        "text": "Intentar descifrar los símbolos",
                        "outcome": "Descubres que estás atrapado en un bucle temporal.",
                        "next_step": 4,
                        "artifact_id": None
                    }
                ]
            }
        ]
    )
    
    adventure = adventure_repository.create(db=db, obj_in=adventure_data)
    logger.info(f"Aventura creada: {adventure.title}")
    
    logger.info("Inicialización de la base de datos completada.") 