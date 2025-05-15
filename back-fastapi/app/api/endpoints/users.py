from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app.api.schemas.user import User, UserUpdate
from app.api.dependencies.auth import get_current_active_user
from app.db.session import get_db
from app.db.repositories.user import user_repository

router = APIRouter()


@router.get("/profile", response_model=User)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Obtiene el perfil del usuario autenticado.
    """
    return current_user


@router.put("/profile", response_model=User)
async def update_user_profile(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Actualiza el perfil del usuario autenticado.
    """
    # Si se intenta actualizar el email, verificar que no exista otro usuario con ese email
    if user_in.email and user_in.email != current_user.email:
        if user_repository.get_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado por otro usuario.",
            )
    
    user = user_repository.update(
        db, db_obj=current_user, obj_in=user_in
    )
    
    return user 