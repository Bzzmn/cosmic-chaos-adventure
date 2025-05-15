from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.session import Base
from app.db.utils import UUID, JSONB

class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    effect = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    characters = relationship("CharacterArtifact", back_populates="artifact")

class CharacterArtifact(Base):
    __tablename__ = "character_artifacts"

    id = Column(UUID, primary_key=True, default=uuid4)
    character_id = Column(UUID, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    artifact_id = Column(UUID, ForeignKey("artifacts.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=False)
    remaining_uses = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    character = relationship("Character", back_populates="artifacts")
    artifact = relationship("Artifact", back_populates="characters") 