"""
Sesión de base de datos con SQLAlchemy.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

from app.core.config import settings

# Configuración del motor de base de datos
engine = create_engine(
    settings.get_database_url(),
    connect_args={"check_same_thread": False} if settings.USE_SQLITE else {}
)

# Configuración para SQLite para asegurar que FOREIGN KEY constraints se respetan
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para obtener una sesión de DB en los endpoints
def get_db():
    """
    Dependency para obtener una sesión de base de datos y cerrarla al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 