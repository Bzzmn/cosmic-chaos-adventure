"""
Configuración de la aplicación

Este módulo contiene la configuración de la aplicación basada en variables de entorno.
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any

# Función helper para parsear booleanos de manera más segura
def parse_bool(value, default=False):
    """Parsea un valor a booleano de manera segura"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("yes", "true", "t", "1", "on")
    return default

class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno."""
    
    # Información de la aplicación
    APP_NAME: str = "Cosmic Chaos Adventure API"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # Usar nuestra función de parseo segura para booleanos en lugar de la validación automática de Pydantic
    @property
    def DEBUG(self) -> bool:
        return parse_bool(os.getenv("DEBUG", "False"))
    
    # Configuración de la base de datos
    # SQLite (default) - más fácil para desarrollo
    @property
    def USE_SQLITE(self) -> bool:
        return parse_bool(os.getenv("USE_SQLITE", "True"))
    
    SQLITE_DB_FILE: str = os.getenv("SQLITE_DB_FILE", "cosmic_chaos.db")
    
    # PostgreSQL - para producción
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "cosmic_chaos")
    
    DATABASE_URL: Optional[str] = None
    
    # Configuración para generación de preguntas
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    @property
    def GENERATE_QUESTIONS_ON_DEMAND(self) -> bool:
        return parse_bool(os.getenv("GENERATE_QUESTIONS_ON_DEMAND", "False"))
    
    @property
    def MIN_QUESTIONS_COUNT(self) -> int:
        try:
            return int(os.getenv("MIN_QUESTIONS_COUNT", "4"))
        except:
            return 4
    
    @property
    def IMAGE_GENERATION_ENABLED(self) -> bool:
        return parse_bool(os.getenv("IMAGE_GENERATION_ENABLED", "False"))
    
    def get_database_url(self) -> str:
        """Retorna la URL de conexión a la base de datos."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        if self.USE_SQLITE:
            return f"sqlite:///{self.SQLITE_DB_FILE}"
        
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # Esto permite campos adicionales en el .env
    }

# Instancia global de configuración
try:
    settings = Settings()
except Exception as e:
    print(f"Error cargando configuración: {str(e)}")
    # Crear una clase simple como fallback
    class SimpleSettings:
        APP_NAME = "Cosmic Chaos Adventure API"
        APP_VERSION = "0.1.0"
        API_PREFIX = "/api"
        DEBUG = False
        USE_SQLITE = True
        SQLITE_DB_FILE = "cosmic_chaos.db"
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        GENERATE_QUESTIONS_ON_DEMAND = parse_bool(os.getenv("GENERATE_QUESTIONS_ON_DEMAND", "False"))
        MIN_QUESTIONS_COUNT = 4
        IMAGE_GENERATION_ENABLED = False
        
        def get_database_url(self):
            return f"sqlite:///{self.SQLITE_DB_FILE}"
    
    settings = SimpleSettings()

# Función para obtener configuraciones de manera segura
def get_setting(name, default=None):
    """Obtiene una configuración de manera segura, devolviendo el valor default si no existe."""
    return getattr(settings, name, default) 