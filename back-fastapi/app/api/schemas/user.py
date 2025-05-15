from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    """Esquema base para usuarios"""
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Esquema para crear usuarios"""
    password: str


class UserSocialLogin(BaseModel):
    """Esquema para login social"""
    provider: str
    token: str


class UserLogin(BaseModel):
    """Esquema para login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Esquema para actualizar usuarios"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    image_url: Optional[str] = None


class UserInDBBase(UserBase):
    """Esquema base para usuarios en la base de datos"""
    id: UUID
    image_url: Optional[str] = None
    provider: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserInDBBase):
    """Esquema para usuarios en la base de datos (incluye password)"""
    password: str


class User(UserInDBBase):
    """Esquema para respuesta de usuario"""
    pass


class UserWithToken(User):
    """Esquema para respuesta de usuario con token"""
    token: str 