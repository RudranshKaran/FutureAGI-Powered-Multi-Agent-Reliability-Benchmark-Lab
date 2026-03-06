"""Evaluation model — stores FutureAGI evaluation results per run."""

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    accuracy: Mapped[float | None] = mapped_column(nullable=True)
    hallucination: Mapped[float | None] = mapped_column(nullable=True)
    coherence: Mapped[float | None] = mapped_column(nullable=True)
    safety: Mapped[float | None] = mapped_column(nullable=True)

    # Relationships
    run: Mapped["Run"] = relationship(back_populates="evaluation")

    def __repr__(self) -> str:
        return f"<Evaluation {self.id} run={self.run_id}>"
