from pydantic import BaseModel


class Token(BaseModel):
    """Esquema para token de autenticación"""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Esquema para payload de token JWT"""
    sub: str 