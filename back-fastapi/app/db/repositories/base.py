from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Repositorio base con operaciones CRUD predefinidas.
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Inicializa el repositorio con un modelo específico.
        
        Args:
            model: Clase del modelo SQLAlchemy.
        """
        self.model = model
    
    def get(self, db: Session, id: UUID) -> Optional[ModelType]:
        """
        Obtiene un registro por su ID.
        
        Args:
            db: Sesión de base de datos.
            id: ID del registro.
            
        Returns:
            El registro encontrado o None si no existe.
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Obtiene múltiples registros con paginación.
        
        Args:
            db: Sesión de base de datos.
            skip: Número de registros a saltar.
            limit: Límite de registros a retornar.
            
        Returns:
            Lista de registros.
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Crea un nuevo registro.
        
        Args:
            db: Sesión de base de datos.
            obj_in: Datos para crear el registro.
            
        Returns:
            El registro creado.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Actualiza un registro existente.
        
        Args:
            db: Sesión de base de datos.
            db_obj: Registro a actualizar.
            obj_in: Datos para actualizar el registro.
            
        Returns:
            El registro actualizado.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: UUID) -> ModelType:
        """
        Elimina un registro por su ID.
        
        Args:
            db: Sesión de base de datos.
            id: ID del registro a eliminar.
            
        Returns:
            El registro eliminado.
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj 