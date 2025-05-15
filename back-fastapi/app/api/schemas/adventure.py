from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class AdventureBase(BaseModel):
    """Esquema base para aventuras"""
    title: str
    steps: List[Dict[str, Any]]


class AdventureCreate(AdventureBase):
    """Esquema para crear aventuras"""
    pass


class AdventureInDBBase(AdventureBase):
    """Esquema base para aventuras en la base de datos"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Adventure(AdventureInDBBase):
    """Esquema para respuesta de aventura"""
    pass


class CharacterProgressBase(BaseModel):
    """Esquema base para progreso de personaje en aventura"""
    character_id: UUID
    adventure_id: UUID
    current_step: int = 0
    choices: List[int] = Field(default_factory=list)
    completed: bool = False


class CharacterProgressCreate(BaseModel):
    """Esquema para guardar progreso en aventura"""
    character_id: UUID
    current_step: int
    choices: List[int]


class CharacterProgressInDB(CharacterProgressBase):
    """Esquema para progreso de personaje en la base de datos"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CharacterProgressResponse(BaseModel):
    """Esquema para respuesta de progreso en aventura"""
    character_id: UUID
    current_step: int
    experience: int
    rewards: List[Dict[str, Any]] = Field(default_factory=list) 