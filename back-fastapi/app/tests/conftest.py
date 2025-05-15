import pytest
from typing import Dict, Generator, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Cambiar la importación para la ubicación correcta de main.py
from main import app
from app.db.session import Base, get_db
from app.api.schemas.personality import PersonalityOptionBase, PersonalityQuestionCreate
from app.db.repositories.personality import personality_repository

# Base de datos en memoria para las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Fixture para crear una sesión de base de datos para las pruebas."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Fixture para crear un cliente de prueba con una sesión de base de datos."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    # Sobreescribir la dependencia get_db para usar la base de datos de prueba
    app.dependency_overrides[get_db] = override_get_db
    
    # Crear datos de prueba
    create_test_data(db)
    
    with TestClient(app) as c:
        yield c
    
    # Limpiar las sobreescrituras de dependencias
    app.dependency_overrides.clear()


def create_test_data(db: Session) -> None:
    """Crear datos de prueba para la base de datos."""
    
    # Crear preguntas de personalidad de prueba
    test_questions = [
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
        )
    ]
    
    for question in test_questions:
        personality_repository.create(db=db, obj_in=question) 