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


# ---------------------------------------------------------------------------
# Experiment status / monitoring models
# ---------------------------------------------------------------------------


class ExperimentStartResponse(BaseModel):
    """Returned immediately when an experiment is launched (runs in background)."""

    experiment_id: str


class ExperimentStatusResponse(BaseModel):
    """Returned by the status polling endpoint."""

    experiment_id: str
    status: str
    architecture: str
    dataset: str
    total_prompts: int
    completed_runs: int
    progress_percentage: float
    avg_tokens: float
    avg_latency_ms: float
    logs: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Experiment results / analytics models
# ---------------------------------------------------------------------------


class DebateTraceEntry(BaseModel):
    """A single debate trace step for display in prompt breakdown."""

    agent_role: str
    turn_number: int
    response: str
    tokens: int
    latency_ms: float


class PromptBreakdown(BaseModel):
    """Per-prompt result with optional debate traces."""

    prompt: str
    final_output: str | None = None
    accuracy: float | None = None
    tokens: int = 0
    latency_ms: float = 0.0
    debate_traces: list[DebateTraceEntry] = Field(default_factory=list)


class ArchitectureComparisonItem(BaseModel):
    architecture: str
    accuracy: float


class TokenAccuracyPoint(BaseModel):
    tokens: int
    accuracy: float


class RoundImprovement(BaseModel):
    rounds: int
    accuracy: float


class ExperimentSummary(BaseModel):
    avg_accuracy: float | None = None
    avg_hallucination: float | None = None
    avg_tokens: float = 0.0
    avg_latency_ms: float = 0.0


class AdvancedMetrics(BaseModel):
    """Research-grade derived metrics for experiment analysis."""

    improvement_per_token: float | None = None
    latency_overhead_percent: float | None = None
    convergence_score: float | None = None
    accuracy_variance: float | None = None
    accuracy_std: float | None = None
    accuracy_mean: float | None = None
    confidence_interval: list[float] | None = None
    stability_score: float | None = None


class ConvergenceTurn(BaseModel):
    """Per-turn similarity data for convergence visualization."""

    turn: int
    similarity: float


class ExperimentResultsResponse(BaseModel):
    """Full analytics response for a completed experiment."""

    experiment_id: str
    architecture: str
    dataset: str
    rounds: int
    summary: ExperimentSummary
    architecture_comparison: list[ArchitectureComparisonItem] = Field(default_factory=list)
    token_accuracy_points: list[TokenAccuracyPoint] = Field(default_factory=list)
    round_improvement: list[RoundImprovement] = Field(default_factory=list)
    prompt_breakdown: list[PromptBreakdown] = Field(default_factory=list)
    advanced_metrics: AdvancedMetrics | None = None
    convergence_turns: list[ConvergenceTurn] = Field(default_factory=list)
