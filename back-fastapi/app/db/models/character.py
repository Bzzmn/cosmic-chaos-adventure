from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.session import Base
from app.db.utils import UUID, JSONB

class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    character_class = Column(String(100), nullable=False)
    image_url = Column(String, nullable=True)
    stats = Column(JSONB, nullable=False, default={})
    experience = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    user = relationship("User", backref="characters")
    artifacts = relationship("CharacterArtifact", back_populates="character", cascade="all, delete-orphan")
    progress = relationship("CharacterProgress", back_populates="character", cascade="all, delete-orphan") 