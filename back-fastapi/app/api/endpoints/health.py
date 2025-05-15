"""
Endpoint para verificar el estado de la API.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Verifica el estado de la API y la conexión a la base de datos.
    """
    # Verificar la conexión a la base de datos
    try:
        # Ejecuta una consulta simple para verificar la conexión
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "ok",
        "database": db_status,
    } 