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


# ---------------------------------------------------------------------------
# Experiment orchestration models
# ---------------------------------------------------------------------------


class ExperimentConfig(BaseModel):
    """Request body for running a full experiment."""

    architecture: str = Field(
        ..., description="Architecture name: single_agent | two_agent_debate | self_refinement"
    )
    dataset: str = Field(..., description="Dataset identifier (e.g. 'arithmetic')")
    model: str = Field(default="gpt-4o", description="LLM model to use")
    rounds: int = Field(default=1, ge=1, description="Number of debate rounds")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")


class EvaluationResult(BaseModel):
    """Structured evaluation metrics returned by FutureAGI."""

    accuracy: float | None = None
    hallucination: float | None = None
    coherence: float | None = None
    safety: float | None = None


class ExperimentResult(BaseModel):
    """Summary returned after an experiment completes."""

    experiment_id: str
    total_runs: int
    avg_tokens: float
    avg_latency_ms: float
    avg_accuracy: float | None = None
    avg_hallucination: float | None = None
    avg_coherence: float | None = None
    avg_safety: float | None = None
