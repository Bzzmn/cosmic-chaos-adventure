from typing import Optional
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.db.models.user import User
from app.api.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    Repositorio para operaciones CRUD de usuarios.
    """
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email.
        
        Args:
            db: Sesión de base de datos.
            email: Email del usuario.
            
        Returns:
            El usuario encontrado o None si no existe.
        """
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Crea un nuevo usuario con contraseña hasheada.
        
        Args:
            db: Sesión de base de datos.
            obj_in: Datos para crear el usuario.
            
        Returns:
            El usuario creado.
        """
        db_obj = User(
            email=obj_in.email,
            name=obj_in.name,
            password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Autentica un usuario verificando email y contraseña.
        
        Args:
            db: Sesión de base de datos.
            email: Email del usuario.
            password: Contraseña en texto plano.
            
        Returns:
            El usuario autenticado o None si la autenticación falla.
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user_repository = UserRepository() 