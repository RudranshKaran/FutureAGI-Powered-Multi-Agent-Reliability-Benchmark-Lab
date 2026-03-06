"""Run model — represents a single prompt execution inside an experiment."""

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.database import Base


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    final_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_tokens: Mapped[int] = mapped_column(default=0)
    total_latency_ms: Mapped[float] = mapped_column(default=0.0)

    # Relationships
    experiment: Mapped["Experiment"] = relationship(back_populates="runs")
    debate_traces: Mapped[list["DebateTrace"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )
    evaluation: Mapped["Evaluation | None"] = relationship(
        back_populates="run", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Run {self.id} exp={self.experiment_id}>"
