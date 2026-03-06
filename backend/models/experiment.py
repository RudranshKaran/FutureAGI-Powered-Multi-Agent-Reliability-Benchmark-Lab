"""Experiment model — represents a single experiment configuration."""

import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from storage.database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    architecture = Column(String, nullable=False)
    rounds = Column(Integer, nullable=False, default=1)
    model = Column(String, nullable=False)
    dataset = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    total_prompts = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    runs = relationship("Run", back_populates="experiment", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Experiment {self.id} arch={self.architecture} status={self.status}>"
