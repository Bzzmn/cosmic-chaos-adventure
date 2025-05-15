from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.repositories.base import BaseRepository
from app.db.models.adventure import Adventure, CharacterProgress
from app.api.schemas.adventure import AdventureCreate, AdventureInDBBase, CharacterProgressCreate, CharacterProgressBase


class AdventureRepository(BaseRepository[Adventure, AdventureCreate, AdventureInDBBase]):
    """
    Repositorio para operaciones CRUD de aventuras.
    """
    
    def __init__(self):
        super().__init__(Adventure)
    
    def get_adventure_steps(self, db: Session, *, adventure_id: UUID) -> List[Dict[str, Any]]:
        """
        Obtiene los pasos de una aventura.
        
        Args:
            db: Sesión de base de datos.
            adventure_id: ID de la aventura.
            
        Returns:
            Lista de pasos de la aventura.
        """
        adventure = self.get(db, id=adventure_id)
        if not adventure:
            return []
        return adventure.steps


class CharacterProgressRepository:
    """
    Repositorio para operaciones de progreso de personaje en aventuras.
    """
    
    def get(self, db: Session, *, character_id: UUID, adventure_id: UUID) -> Optional[CharacterProgress]:
        """
        Obtiene el progreso de un personaje en una aventura específica.
        
        Args:
            db: Sesión de base de datos.
            character_id: ID del personaje.
            adventure_id: ID de la aventura.
            
        Returns:
            El progreso si existe, None en caso contrario.
        """
        return db.query(CharacterProgress).filter(
            CharacterProgress.character_id == character_id,
            CharacterProgress.adventure_id == adventure_id
        ).first()
    
    def get_by_character(self, db: Session, *, character_id: UUID) -> List[CharacterProgress]:
        """
        Obtiene todo el progreso de un personaje en todas las aventuras.
        
        Args:
            db: Sesión de base de datos.
            character_id: ID del personaje.
            
        Returns:
            Lista de progreso del personaje.
        """
        return db.query(CharacterProgress).filter(
            CharacterProgress.character_id == character_id
        ).all()
    
    def create_or_update(
        self, 
        db: Session, 
        *, 
        obj_in: CharacterProgressCreate
    ) -> CharacterProgress:
        """
        Crea o actualiza el progreso de un personaje en una aventura.
        
        Args:
            db: Sesión de base de datos.
            obj_in: Datos para crear/actualizar el progreso.
            
        Returns:
            El progreso creado o actualizado.
        """
        # Verificar si ya existe un progreso para esta combinación de personaje y aventura
        progress = self.get(
            db, 
            character_id=obj_in.character_id, 
            adventure_id=obj_in.adventure_id
        )
        
        if progress:
            # Actualizar progreso existente
            for field, value in obj_in.dict().items():
                setattr(progress, field, value)
                
            # Verificar si el personaje ha completado la aventura (lógica específica)
            # Esto dependerá de la estructura de la aventura
            
            db.add(progress)
            db.commit()
            db.refresh(progress)
            return progress
        else:
            # Crear nuevo progreso
            db_obj = CharacterProgress(**obj_in.dict())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
    
    def calculate_rewards(self, character_progress: CharacterProgress, adventure: Adventure) -> Dict[str, Any]:
        """
        Calcula las recompensas basadas en el progreso del personaje y la aventura.
        
        Args:
            character_progress: Progreso del personaje.
            adventure: Aventura completada o en progreso.
            
        Returns:
            Diccionario con las recompensas calculadas.
        """
        # Esta función implementaría la lógica para calcular recompensas
        # basado en las elecciones hechas por el personaje y la estructura de la aventura
        
        # Por ahora, retornamos recompensas simuladas
        rewards = []
        
        # Ejemplo de cálculo de recompensas basado en el paso actual
        if character_progress.current_step > 3:
            rewards.append({
                "type": "experience",
                "value": 50 * character_progress.current_step
            })
        
        if character_progress.current_step > 5:
            rewards.append({
                "type": "artifact",
                "id": "some-artifact-id",
                "name": "Artefacto de ejemplo"
            })
        
        return rewards


adventure_repository = AdventureRepository()
character_progress_repository = CharacterProgressRepository() 