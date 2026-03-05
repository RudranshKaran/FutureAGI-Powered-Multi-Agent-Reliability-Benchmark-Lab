"""
Pydantic schemas for request/response models.

These are used by the LLM service, architecture layer, and API endpoints.
"""

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# LLM Service response
# ---------------------------------------------------------------------------


class LLMResponse(BaseModel):
    """Structured response from a single LLM call."""

    response_text: str
    tokens_used: int
    latency_ms: float


# ---------------------------------------------------------------------------
# Architecture result objects
# ---------------------------------------------------------------------------


class ArchitectureStep(BaseModel):
    """A single reasoning step within an architecture execution."""

    agent: str
    turn: int
    response: str
    tokens: int
    latency_ms: float


class ArchitectureResult(BaseModel):
    """Aggregate result returned by every architecture implementation."""

    final_output: str
    total_tokens: int
    total_latency_ms: float
    steps: list[ArchitectureStep] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# API request models
# ---------------------------------------------------------------------------


class TestArchitectureRequest(BaseModel):
    """Request body for the /test-architecture endpoint."""

    architecture: str = Field(
        ..., description="Architecture name: single_agent | two_agent_debate | self_refinement"
    )
    prompt: str = Field(..., description="The input prompt to run through the architecture")
    rounds: int = Field(default=1, ge=1, description="Number of debate rounds (used by debate architectures)")
