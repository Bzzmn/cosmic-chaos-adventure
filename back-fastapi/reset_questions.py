import os
from app.db.session import SessionLocal, engine
from app.db.models.personality import PersonalityQuestion
from sqlalchemy.exc import SQLAlchemyError

def reset_personality_questions():
    """Elimina todas las preguntas de personalidad de la base de datos"""
    db = SessionLocal()
    try:
        # Eliminar todas las preguntas existentes
        num_deleted = db.query(PersonalityQuestion).delete()
        db.commit()
        print(f"Se han eliminado {num_deleted} preguntas de personalidad.")
        print("La próxima solicitud al endpoint generará nuevas preguntas.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al eliminar preguntas: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # Configurar variables de entorno para asegurar la generación
    os.environ["GENERATE_QUESTIONS_ON_DEMAND"] = "True"
    os.environ["MIN_QUESTIONS_COUNT"] = "10"
    os.environ["IMAGE_GENERATION_ENABLED"] = "True"
    
    # Eliminar preguntas existentes
    reset_personality_questions() 