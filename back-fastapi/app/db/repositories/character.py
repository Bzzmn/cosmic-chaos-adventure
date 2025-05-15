from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.repositories.base import BaseRepository
from app.db.models.character import Character
from app.api.schemas.character import CharacterCreate, CharacterUpdate


class CharacterRepository(BaseRepository[Character, CharacterCreate, CharacterUpdate]):
    """
    Repositorio para operaciones CRUD de personajes.
    """
    
    def __init__(self):
        super().__init__(Character)
    
    def get_by_user_id(self, db: Session, *, user_id: UUID) -> List[Character]:
        """
        Obtiene todos los personajes de un usuario.
        
        Args:
            db: Sesión de base de datos.
            user_id: ID del usuario.
            
        Returns:
            Lista de personajes del usuario.
        """
        return db.query(Character).filter(Character.user_id == user_id).all()
    
    def create_with_user(self, db: Session, *, obj_in: CharacterCreate, user_id: UUID) -> Character:
        """
        Crea un nuevo personaje asociado a un usuario.
        
        Args:
            db: Sesión de base de datos.
            obj_in: Datos para crear el personaje.
            user_id: ID del usuario propietario.
            
        Returns:
            El personaje creado.
        """
        obj_in_data = obj_in.dict()
        obj_in_data["user_id"] = user_id
        db_obj = Character(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_user_character(self, db: Session, *, user_id: UUID, character_id: UUID) -> Optional[Character]:
        """
        Obtiene un personaje específico de un usuario.
        
        Args:
            db: Sesión de base de datos.
            user_id: ID del usuario.
            character_id: ID del personaje.
            
        Returns:
            El personaje si existe y pertenece al usuario, None en caso contrario.
        """
        return db.query(Character).filter(
            Character.id == character_id,
            Character.user_id == user_id
        ).first()


character_repository = CharacterRepository() 