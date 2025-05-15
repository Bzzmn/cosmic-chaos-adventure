from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
import secrets
from uuid import UUID

from app.core.config import settings

# Contexto para encriptar y verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generador de tokens para reseteo de contraseñas o verificación de email
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 8 días


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Crea un token JWT de acceso.
    
    Args:
        subject: Identificador del usuario (generalmente id).
        expires_delta: Tiempo de expiración opcional.
        
    Returns:
        Token JWT encodado.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña plana coincide con la contraseña hasheada.
    
    Args:
        plain_password: Contraseña en texto plano.
        hashed_password: Contraseña hasheada.
        
    Returns:
        True si coinciden, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash de contraseña.
    
    Args:
        password: Contraseña en texto plano.
        
    Returns:
        Hash de la contraseña.
    """
    return pwd_context.hash(password) 