from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.repositories.base import BaseRepository
from app.db.models.artifact import Artifact, CharacterArtifact
from app.api.schemas.artifact import ArtifactCreate, ArtifactUpdate, CharacterArtifactCreate, CharacterArtifactUpdate


class ArtifactRepository(BaseRepository[Artifact, ArtifactCreate, ArtifactUpdate]):
    """
    Repositorio para operaciones CRUD de artefactos.
    """
    
    def __init__(self):
        super().__init__(Artifact)


class CharacterArtifactRepository:
    """
    Repositorio para operaciones de la relación entre personajes y artefactos.
    """
    
    def get(self, db: Session, *, character_id: UUID, artifact_id: UUID) -> Optional[CharacterArtifact]:
        """
        Obtiene una relación personaje-artefacto específica.
        
        Args:
            db: Sesión de base de datos.
            character_id: ID del personaje.
            artifact_id: ID del artefacto.
            
        Returns:
            La relación si existe, None en caso contrario.
        """
        return db.query(CharacterArtifact).filter(
            CharacterArtifact.character_id == character_id,
            CharacterArtifact.artifact_id == artifact_id
        ).first()
    
    def get_by_character(self, db: Session, *, character_id: UUID) -> List[CharacterArtifact]:
        """
        Obtiene todos los artefactos de un personaje.
        
        Args:
            db: Sesión de base de datos.
            character_id: ID del personaje.
            
        Returns:
            Lista de relaciones personaje-artefacto.
        """
        return db.query(CharacterArtifact).filter(
            CharacterArtifact.character_id == character_id
        ).all()
    
    def create(self, db: Session, *, obj_in: CharacterArtifactCreate, character_id: UUID) -> CharacterArtifact:
        """
        Crea una nueva relación entre un personaje y un artefacto.
        
        Args:
            db: Sesión de base de datos.
            obj_in: Datos para crear la relación.
            character_id: ID del personaje.
            
        Returns:
            La relación creada.
        """
        db_obj = CharacterArtifact(
            character_id=character_id,
            artifact_id=obj_in.artifact_id,
            is_active=False
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: CharacterArtifact, obj_in: CharacterArtifactUpdate) -> CharacterArtifact:
        """
        Actualiza una relación personaje-artefacto.
        
        Args:
            db: Sesión de base de datos.
            db_obj: Relación a actualizar.
            obj_in: Datos para actualizar la relación.
            
        Returns:
            La relación actualizada.
        """
        update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, db_obj: CharacterArtifact) -> CharacterArtifact:
        """
        Elimina una relación personaje-artefacto.
        
        Args:
            db: Sesión de base de datos.
            db_obj: Relación a eliminar.
            
        Returns:
            La relación eliminada.
        """
        obj = db_obj
        db.delete(obj)
        db.commit()
        return obj


artifact_repository = ArtifactRepository()
character_artifact_repository = CharacterArtifactRepository() 