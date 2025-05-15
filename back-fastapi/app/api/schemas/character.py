from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class CharacterBase(BaseModel):
    """Esquema base para personajes"""
    name: str
    character_class: str
    image_url: Optional[str] = None
    stats: Dict[str, Any] = Field(default_factory=dict)


class CharacterCreate(CharacterBase):
    """Esquema para crear personajes"""
    user_id: Optional[UUID] = None


class CharacterUpdate(BaseModel):
    """Esquema para actualizar personajes"""
    name: Optional[str] = None
    image_url: Optional[str] = None
    stats: Optional[Dict[str, Any]] = None
    experience: Optional[int] = None


class CharacterInDBBase(CharacterBase):
    """Esquema base para personajes en la base de datos"""
    id: UUID
    user_id: UUID
    experience: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Character(CharacterInDBBase):
    """Esquema para respuesta de personaje (incluye relaciones)"""
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)


class CharacterList(BaseModel):
    """Esquema para listar personajes"""
    items: List[Character]
    total: int 