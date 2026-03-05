"""Run model — represents a single prompt execution inside an experiment."""

import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from storage.database import Base


class Run(Base):
    __tablename__ = "runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id = Column(
        UUID(as_uuid=True), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )
    prompt = Column(Text, nullable=False)
    final_output = Column(Text, nullable=True)
    total_tokens = Column(Integer, default=0)
    total_latency_ms = Column(Float, default=0.0)

    # Relationships
    experiment = relationship("Experiment", back_populates="runs")
    debate_traces = relationship(
        "DebateTrace", back_populates="run", cascade="all, delete-orphan"
    )
    evaluation = relationship(
        "Evaluation", back_populates="run", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Run {self.id} exp={self.experiment_id}>"
