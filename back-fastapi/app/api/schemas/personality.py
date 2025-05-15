from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class PersonalityOptionBase(BaseModel):
    """Esquema base para opciones de preguntas de personalidad"""
    text: str
    emoji: Optional[str] = None
    value: int
    effect: Dict[str, int]
    feedback: Optional[str] = None


class PersonalityQuestionBase(BaseModel):
    """Esquema base para preguntas de personalidad"""
    question: str
    options: List[PersonalityOptionBase]
    context_image: Optional[str] = None
    scenario_description: Optional[str] = None


class PersonalityQuestionCreate(PersonalityQuestionBase):
    """Esquema para crear preguntas de personalidad"""
    pass


class PersonalityQuestionInDBBase(PersonalityQuestionBase):
    """Esquema base para preguntas de personalidad en la base de datos"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PersonalityQuestion(PersonalityQuestionInDBBase):
    """Esquema para respuesta de pregunta de personalidad"""
    pass


class PersonalityQuestionList(BaseModel):
    """Esquema para listar preguntas de personalidad"""
    items: List[PersonalityQuestion]
    total: int


class PersonalityTestSubmit(BaseModel):
    """Esquema para enviar resultados del test de personalidad"""
    user_id: UUID
    answers: List[int]


class PersonalityStats(BaseModel):
    """Esquema para estadísticas de personalidad"""
    quantum_charisma: int = 0
    absurdity_resistance: int = 0
    sarcasm_level: int = 0
    time_warping: int = 0
    cosmic_luck: int = 0


class PersonalityTestResults(BaseModel):
    """Esquema para resultados del test de personalidad"""
    stats: PersonalityStats 