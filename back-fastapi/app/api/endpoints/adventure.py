from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List, Dict
from uuid import UUID

from app.api.schemas.adventure import (
    Adventure, CharacterProgressCreate, CharacterProgressResponse
)
from app.api.dependencies.auth import get_current_active_user
from app.api.schemas.user import User
from app.db.session import get_db
from app.db.repositories.adventure import adventure_repository, character_progress_repository
from app.db.repositories.character import character_repository

router = APIRouter()


@router.get("/story", response_model=List[Dict])
async def get_adventure_story(
    *,
    db: Session = Depends(get_db),
    adventure_id: UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtiene los pasos de una historia de aventura.
    """
    # Verificar que la aventura existe
    adventure = adventure_repository.get(db=db, id=adventure_id)
    if not adventure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aventura no encontrada",
        )
    
    # Obtener los pasos de la aventura
    steps = adventure_repository.get_adventure_steps(db=db, adventure_id=adventure_id)
    return steps


@router.post("/progress", response_model=CharacterProgressResponse)
async def save_adventure_progress(
    *,
    db: Session = Depends(get_db),
    progress: CharacterProgressCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Guarda el progreso de un personaje en una aventura.
    """
    # Verificar que el personaje existe y pertenece al usuario
    character = character_repository.get_user_character(
        db=db, user_id=current_user.id, character_id=progress.character_id
    )
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personaje no encontrado",
        )
    
    # Verificar que la aventura existe
    adventure = adventure_repository.get(db=db, id=progress.adventure_id)
    if not adventure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aventura no encontrada",
        )
    
    # Guardar o actualizar el progreso
    saved_progress = character_progress_repository.create_or_update(
        db=db, obj_in=progress
    )
    
    # Calcular recompensas basadas en el progreso
    rewards = character_progress_repository.calculate_rewards(
        character_progress=saved_progress, adventure=adventure
    )
    
    # Aplicar recompensas (por ejemplo, experiencia)
    for reward in rewards:
        if reward["type"] == "experience":
            character.experience += reward["value"]
    
    # Guardar los cambios del personaje
    db.add(character)
    db.commit()
    db.refresh(character)
    
    # Crear respuesta
    response = CharacterProgressResponse(
        character_id=character.id,
        current_step=saved_progress.current_step,
        experience=character.experience,
        rewards=rewards
    )
    
    return response 