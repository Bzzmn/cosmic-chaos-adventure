from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.core.security import SECRET_KEY, ALGORITHM
from app.api.schemas.token import TokenPayload
from app.api.schemas.user import User
from app.db.session import get_db
from app.db.models.user import User as UserModel
from app.core.config import settings

# Configuración del esquema OAuth2 para autenticación
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/login"
)


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency para obtener el usuario actual a partir del token JWT.
    
    Args:
        db: Sesión de base de datos.
        token: Token JWT.
        
    Returns:
        Usuario actual.
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe.
    """
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(UserModel).filter(UserModel.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency para verificar que el usuario actual esté activo.
    
    Args:
        current_user: Usuario actual.
        
    Returns:
        Usuario actual si está activo.
        
    Raises:
        HTTPException: Si el usuario no está activo.
    """
    # Aquí se puede agregar lógica adicional para verificar si el usuario está activo
    return current_user 