"""Experiment model — represents a single experiment configuration."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    architecture: Mapped[str] = mapped_column(String, nullable=False)
    rounds: Mapped[int] = mapped_column(nullable=False, default=1)
    model: Mapped[str] = mapped_column(String, nullable=False)
    dataset: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    total_prompts: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    runs: Mapped[list["Run"]] = relationship(back_populates="experiment", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Experiment {self.id} arch={self.architecture} status={self.status}>"
