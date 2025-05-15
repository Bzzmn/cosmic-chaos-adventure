"""
Punto de entrada principal para la aplicación FastAPI.
"""

import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import JSONResponse

from app.api.router import router as api_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.init_db import init_db

# Configurar logging
logger = logging.getLogger("cosmic-chaos")
logging.basicConfig(level=logging.INFO)

def create_application() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    """
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG
    )
    
    # Configurar CORS - con opciones más permisivas para desarrollo
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permitir todos los orígenes
        allow_credentials=True,
        allow_methods=["*"],  # Permitir todos los métodos
        allow_headers=["*"],  # Permitir todos los headers
        expose_headers=["*"],  # Exponer todos los headers en la respuesta
        max_age=86400,       # Tiempo de caché para preflight
    )
    
    # Middleware para añadir explicitamente headers CORS en cada respuesta (para ngrok)
    @application.middleware("http")
    async def add_cors_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    
    # Middleware para manejar excepciones y añadir headers CORS
    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Error no manejado: {str(exc)}")
        response = JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Incluir routers
    application.include_router(api_router, prefix=settings.API_PREFIX)
    
    @application.get("/")
    async def root():
        """
        Endpoint raíz para verificar que la API está funcionando.
        """
        return {"message": "¡Hola, mundo! Bienvenido a Cosmic Chaos Adventure API"}
    
    # Configurar directorio estático para imágenes generadas
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    images_dir = static_dir / "images" / "generated"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Montar directorio estático
    application.mount("/static", StaticFiles(directory="static"), name="static")
    
    return application

app = create_application()

# Inicializar la base de datos con datos de ejemplo
@app.on_event("startup")
async def startup_db_client():
    """
    Inicializa la base de datos al iniciar la aplicación.
    """
    db = SessionLocal()
    try:
        init_db(db)
        # Mostrar la URL de la aplicación
        host = "0.0.0.0"
        port = 8000
        logger.info("="*60)
        logger.info(f"🚀 Cosmic Chaos Adventure API está funcionando en:")
        logger.info(f"🌐 http://localhost:{port}")
        logger.info(f"🌐 http://localhost:{port}/docs - Documentación Swagger")
        logger.info(f"🌐 http://localhost:{port}/redoc - Documentación ReDoc")
        logger.info(f"🔍 La base de datos está utilizando: {'SQLite' if settings.USE_SQLITE else 'PostgreSQL'}")
        logger.info("="*60)
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    