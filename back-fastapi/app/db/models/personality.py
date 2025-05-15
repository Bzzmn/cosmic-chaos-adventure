from sqlalchemy import Column, String, DateTime, func
from uuid import uuid4

from app.db.session import Base
from app.db.utils import UUID, JSONB

class PersonalityQuestion(Base):
    __tablename__ = "personality_questions"

    id = Column(UUID, primary_key=True, default=uuid4)
    question = Column(String, nullable=False)
    options = Column(JSONB, nullable=False)
    context_image = Column(String, nullable=True)
    scenario_description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 