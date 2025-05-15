from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class ArtifactEffect(BaseModel):
    """Esquema para efecto de artefacto"""
    stat: str
    bonus: int
    duration: Optional[int] = None


class ArtifactBase(BaseModel):
    """Esquema base para artefactos"""
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    effect: Dict[str, Any]


class ArtifactCreate(ArtifactBase):
    """Esquema para crear artefactos"""
    pass


class ArtifactUpdate(BaseModel):
    """Esquema para actualizar artefactos"""
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    effect: Optional[Dict[str, Any]] = None


class ArtifactInDBBase(ArtifactBase):
    """Esquema base para artefactos en la base de datos"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Artifact(ArtifactInDBBase):
    """Esquema para respuesta de artefacto"""
    pass


class ArtifactList(BaseModel):
    """Esquema para listar artefactos"""
    items: List[Artifact]
    total: int


class CharacterArtifactBase(BaseModel):
    """Esquema base para relación personaje-artefacto"""
    character_id: UUID
    artifact_id: UUID
    is_active: bool = False
    remaining_uses: Optional[int] = None


class CharacterArtifactCreate(BaseModel):
    """Esquema para asignar artefacto a personaje"""
    artifact_id: UUID


class CharacterArtifactUpdate(BaseModel):
    """Esquema para actualizar estado de artefacto en personaje"""
    is_active: bool


class CharacterArtifactInDB(CharacterArtifactBase):
    """Esquema para relación personaje-artefacto en la base de datos"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 