from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from uuid import UUID

from app.api.schemas.artifact import (
    Artifact, ArtifactList, CharacterArtifactCreate, 
    CharacterArtifactUpdate
)
from app.api.schemas.character import Character
from app.api.dependencies.auth import get_current_active_user
from app.api.schemas.user import User
from app.db.session import get_db
from app.db.repositories.artifact import artifact_repository, character_artifact_repository
from app.db.repositories.character import character_repository

router = APIRouter()


@router.get("", response_model=List[Artifact])
async def get_artifacts(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Obtiene la lista de artefactos disponibles.
    Este endpoint es público y no requiere autenticación.
    """
    artifacts = artifact_repository.get_multi(db, skip=skip, limit=limit)
    return artifacts


@router.post("/characters/{character_id}/artifacts", response_model=Character)
async def add_artifact_to_character(
    *,
    db: Session = Depends(get_db),
    character_id: UUID,
    artifact_in: CharacterArtifactCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Agrega un artefacto a un personaje.
    """
    # Verificar que el personaje existe y pertenece al usuario
    character = character_repository.get_user_character(
        db=db, user_id=current_user.id, character_id=character_id
    )
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personaje no encontrado",
        )
    
    # Verificar que el artefacto existe
    artifact = artifact_repository.get(db=db, id=artifact_in.artifact_id)
    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artefacto no encontrado",
        )
    
    # Verificar si el personaje ya tiene este artefacto
    existing_artifact = character_artifact_repository.get(
        db=db, character_id=character_id, artifact_id=artifact_in.artifact_id
    )
    if existing_artifact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El personaje ya tiene este artefacto",
        )
    
    # Crear la relación entre personaje y artefacto
    character_artifact_repository.create(
        db=db, obj_in=artifact_in, character_id=character_id
    )
    
    # Obtener el personaje actualizado
    character = character_repository.get(db=db, id=character_id)
    return character


@router.put("/characters/{character_id}/artifacts/{artifact_id}", response_model=Character)
async def update_character_artifact(
    *,
    db: Session = Depends(get_db),
    character_id: UUID,
    artifact_id: UUID,
    artifact_in: CharacterArtifactUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Actualiza el estado de un artefacto de un personaje (activar/desactivar).
    """
    # Verificar que el personaje existe y pertenece al usuario
    character = character_repository.get_user_character(
        db=db, user_id=current_user.id, character_id=character_id
    )
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personaje no encontrado",
        )
    
    # Verificar que el artefacto existe y pertenece al personaje
    character_artifact = character_artifact_repository.get(
        db=db, character_id=character_id, artifact_id=artifact_id
    )
    if not character_artifact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El personaje no tiene este artefacto",
        )
    
    # Actualizar el estado del artefacto
    character_artifact_repository.update(
        db=db, db_obj=character_artifact, obj_in=artifact_in
    )
    
    # Obtener el personaje actualizado
    character = character_repository.get(db=db, id=character_id)
    return character 