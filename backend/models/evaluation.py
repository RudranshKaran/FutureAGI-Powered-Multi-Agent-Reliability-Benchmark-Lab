"""Evaluation model — stores FutureAGI evaluation results per run."""

import uuid

from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from storage.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(
        UUID(as_uuid=True),
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    accuracy = Column(Float, nullable=True)
    hallucination = Column(Float, nullable=True)
    coherence = Column(Float, nullable=True)
    safety = Column(Float, nullable=True)

    # Relationships
    run = relationship("Run", back_populates="evaluation")

    def __repr__(self) -> str:
        return f"<Evaluation {self.id} run={self.run_id}>"
