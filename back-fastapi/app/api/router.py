"""
API Router principal

Este módulo contiene el router principal que agrega todos los endpoints de la API.
"""

from fastapi import APIRouter

from app.api.endpoints import (
    auth, users, health, characters, 
    artifacts, personality, adventure
)

router = APIRouter()

# Incluir los routers específicos
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(characters.router, prefix="/characters", tags=["characters"])
router.include_router(artifacts.router, prefix="/artifacts", tags=["artifacts"])
router.include_router(personality.router, prefix="/personality", tags=["personality"])
router.include_router(adventure.router, prefix="/adventure", tags=["adventure"])
router.include_router(health.router, tags=["health"]) 