"""DebateTrace model — stores intermediate agent reasoning steps."""

import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from storage.database import Base


class DebateTrace(Base):
    __tablename__ = "debate_traces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(
        UUID(as_uuid=True), ForeignKey("runs.id", ondelete="CASCADE"), nullable=False
    )
    agent_role = Column(String, nullable=False)
    turn_number = Column(Integer, nullable=False)
    response = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)

    # Relationships
    run = relationship("Run", back_populates="debate_traces")

    def __repr__(self) -> str:
        return f"<DebateTrace {self.id} run={self.run_id} turn={self.turn_number}>"
