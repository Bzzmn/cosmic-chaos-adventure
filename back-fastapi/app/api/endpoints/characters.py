from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from uuid import UUID

from app.api.schemas.character import Character, CharacterCreate, CharacterUpdate, CharacterList
from app.api.dependencies.auth import get_current_active_user
from app.api.schemas.user import User
from app.db.session import get_db
from app.db.repositories.character import character_repository

router = APIRouter()


@router.post("", response_model=Character, status_code=status.HTTP_201_CREATED)
async def create_character(
    *,
    db: Session = Depends(get_db),
    character_in: CharacterCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Crea un nuevo personaje para el usuario autenticado.
    """
    character = character_repository.create_with_user(
        db=db, obj_in=character_in, user_id=current_user.id
    )
    return character


@router.get("", response_model=List[Character])
async def get_characters(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Obtiene todos los personajes del usuario autenticado.
    """
    characters = character_repository.get_by_user_id(
        db=db, user_id=current_user.id
    )
    return characters


@router.get("/{character_id}", response_model=Character)
async def get_character(
    *,
    db: Session = Depends(get_db),
    character_id: UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtiene un personaje específico del usuario autenticado.
    """
    character = character_repository.get_user_character(
        db=db, user_id=current_user.id, character_id=character_id
    )
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personaje no encontrado",
        )
    return character


@router.put("/{character_id}", response_model=Character)
async def update_character(
    *,
    db: Session = Depends(get_db),
    character_id: UUID,
    character_in: CharacterUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Actualiza un personaje específico del usuario autenticado.
    """
    character = character_repository.get_user_character(
        db=db, user_id=current_user.id, character_id=character_id
    )
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personaje no encontrado",
        )
    
    character = character_repository.update(
        db=db, db_obj=character, obj_in=character_in
    )
    return character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    *,
    db: Session = Depends(get_db),
    character_id: UUID,
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Elimina un personaje específico del usuario autenticado.
    """
    character = character_repository.get_user_character(
        db=db, user_id=current_user.id, character_id=character_id
    )
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personaje no encontrado",
        )
    
    character_repository.remove(db=db, id=character_id) 