"""
Modelos de SQLAlchemy para la base de datos.

Importa aquí todos los modelos para que puedan ser accedidos desde 'app.db.models'.
"""

from app.db.models.user import User
from app.db.models.character import Character
from app.db.models.artifact import Artifact, CharacterArtifact
from app.db.models.adventure import Adventure, CharacterProgress
from app.db.models.personality import PersonalityQuestion

# Ejemplo: from app.db.models.user import User 