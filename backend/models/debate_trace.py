"""DebateTrace model — stores intermediate agent reasoning steps."""

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.database import Base


class DebateTrace(Base):
    __tablename__ = "debate_traces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("runs.id", ondelete="CASCADE"), nullable=False
    )
    agent_role: Mapped[str] = mapped_column(String, nullable=False)
    turn_number: Mapped[int] = mapped_column(nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    tokens: Mapped[int] = mapped_column(default=0)
    latency_ms: Mapped[float] = mapped_column(default=0.0)

    # Relationships
    run: Mapped["Run"] = relationship(back_populates="debate_traces")

    def __repr__(self) -> str:
        return f"<DebateTrace {self.id} run={self.run_id} turn={self.turn_number}>"
