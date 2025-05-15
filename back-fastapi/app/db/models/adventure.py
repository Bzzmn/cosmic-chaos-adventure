from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.session import Base
from app.db.utils import UUID, JSONB

class Adventure(Base):
    __tablename__ = "adventures"

    id = Column(UUID, primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    steps = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    character_progress = relationship("CharacterProgress", back_populates="adventure", cascade="all, delete-orphan")


class CharacterProgress(Base):
    __tablename__ = "character_progress"

    id = Column(UUID, primary_key=True, default=uuid4)
    character_id = Column(UUID, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    adventure_id = Column(UUID, ForeignKey("adventures.id", ondelete="CASCADE"), nullable=False)
    current_step = Column(Integer, nullable=False, default=0)
    choices = Column(JSONB, default=[])
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    character = relationship("Character", back_populates="progress")
    adventure = relationship("Adventure", back_populates="character_progress") 