from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.api.schemas.user import User, UserCreate, UserWithToken
from app.api.schemas.token import Token
from app.core.security import create_access_token
from app.db.session import get_db
from app.db.repositories.user import user_repository

router = APIRouter()


@router.post("/register", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def register(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """
    Registra un nuevo usuario.
    """
    user = user_repository.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado.",
        )
    
    user = user_repository.create(db, obj_in=user_in)
    
    # Crear token de acceso
    access_token = create_access_token(subject=str(user.id))
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "image_url": user.image_url,
        "provider": user.provider,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "token": access_token
    }


@router.post("/login", response_model=UserWithToken)
async def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Autentica un usuario con email y contraseña.
    """
    user = user_repository.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token = create_access_token(subject=str(user.id))
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "image_url": user.image_url,
        "provider": user.provider,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "token": access_token
    }


@router.post("/social-login", response_model=UserWithToken)
async def social_login(
    *, db: Session = Depends(get_db), provider_data: dict
) -> Any:
    """
    Autentica un usuario con un proveedor social (Google, Facebook, etc.).
    """
    # Este endpoint se implementaría según las necesidades específicas de integración
    # con proveedores de autenticación social como Google, Facebook, etc.
    
    # Por ahora, se devuelve un error indicando que no está implementado
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="La autenticación social no está implementada aún",
    ) 