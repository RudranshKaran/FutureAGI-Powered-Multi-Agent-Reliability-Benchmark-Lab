"""
Advanced metrics engine for research-grade experiment analysis.

Computes derived metrics from existing Run, Evaluation, DebateTrace,
and Experiment data — no additional database schema required.
"""

import difflib
import logging
import math
import statistics
from typing import Optional

from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from models.debate_trace import DebateTrace
from models.evaluation import Evaluation
from models.experiment import Experiment
from models.run import Run
from models.schemas import AdvancedMetrics, ConvergenceTurn

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Individual metric computations
# ---------------------------------------------------------------------------


def compute_improvement_per_token(
    accuracy: float,
    baseline_accuracy: float,
    total_tokens: float,
) -> Optional[float]:
    """Accuracy gain per token consumed relative to single-agent baseline."""
    if total_tokens <= 0:
        return None
    return (accuracy - baseline_accuracy) / total_tokens


def compute_latency_overhead(
    latency: float,
    baseline_latency: float,
) -> Optional[float]:
    """Percentage latency increase compared to single-agent baseline."""
    if baseline_latency <= 0:
        return None
    return ((latency - baseline_latency) / baseline_latency) * 100


def compute_convergence_score(initial_text: str, final_text: str) -> float:
    """Similarity between initial and final debate answers (0-1).

    Uses ``difflib.SequenceMatcher`` which is stdlib and zero-dependency.
    Can be swapped later for embedding-based cosine similarity if needed.
    """
    if not initial_text or not final_text:
        return 0.0
    return difflib.SequenceMatcher(None, initial_text, final_text).ratio()


def compute_convergence_turns(traces: list[tuple[int, str]]) -> list[ConvergenceTurn]:
    """Per-turn similarity series for convergence chart.

    ``traces`` is a list of (turn_number, response_text) sorted by turn.
    Each turn's similarity is measured against the *previous* turn.
    """
    if len(traces) < 2:
        return []

    turns: list[ConvergenceTurn] = []
    for i in range(1, len(traces)):
        sim = difflib.SequenceMatcher(
            None, traces[i - 1][1], traces[i][1]
        ).ratio()
        turns.append(ConvergenceTurn(turn=traces[i][0], similarity=round(sim, 4)))
    return turns


def compute_variance_and_std(
    scores: list[float],
) -> tuple[Optional[float], Optional[float]]:
    """Variance and standard deviation of accuracy scores.

    Requires at least 2 values; returns ``(None, None)`` otherwise.
    """
    if len(scores) < 2:
        return None, None
    var = statistics.variance(scores)
    std = statistics.stdev(scores)
    return round(var, 6), round(std, 6)


def compute_confidence_interval(
    mean: float,
    std: float,
    n: int,
) -> Optional[list[float]]:
    """95 % confidence interval for the mean accuracy.

    Requires ``n >= 2``.
    """
    if n < 2 or std <= 0:
        return None
    margin = 1.96 * (std / math.sqrt(n))
    lower = max(0.0, round(mean - margin, 4))
    upper = min(1.0, round(mean + margin, 4))
    return [lower, upper]


def compute_stability_score(
    accuracy_mean: float,
    hallucination_rate: float,
    accuracy_variance: float,
) -> float:
    """Composite stability metric in [0, 1].

    ``accuracy_mean * (1 − hallucination_rate) * (1 − accuracy_variance)``
    Clamped to ``[0, 1]``.
    """
    raw = accuracy_mean * (1 - hallucination_rate) * (1 - accuracy_variance)
    return round(max(0.0, min(1.0, raw)), 4)


# ---------------------------------------------------------------------------
# Orchestrator — queries DB and assembles all advanced metrics
# ---------------------------------------------------------------------------


def compute_advanced_metrics(
    db: Session,
    experiment: Experiment,
) -> tuple[AdvancedMetrics, list[ConvergenceTurn]]:
    """Compute all advanced metrics for a completed experiment.

    Returns ``(AdvancedMetrics, convergence_turns)`` ready to attach to
    the ``ExperimentResultsResponse``.
    """

    exp_id = experiment.id

    # ------------------------------------------------------------------
    # 1. Current experiment aggregates
    # ------------------------------------------------------------------
    agg = (
        db.query(
            sa_func.avg(Evaluation.accuracy),
            sa_func.avg(Evaluation.hallucination),
            sa_func.avg(Run.total_tokens),
            sa_func.avg(Run.total_latency_ms),
        )
        .join(Run, Evaluation.run_id == Run.id)
        .filter(Run.experiment_id == exp_id)
        .first()
    )

    if agg is None or agg[0] is None:
        return AdvancedMetrics(), []

    exp_accuracy = float(agg[0])
    exp_hallucination = float(agg[1] or 0)
    exp_tokens = float(agg[2] or 0)
    exp_latency = float(agg[3] or 0)

    # ------------------------------------------------------------------
    # 2. Baseline — single_agent on the same dataset
    # ------------------------------------------------------------------
    baseline_row = (
        db.query(
            sa_func.avg(Evaluation.accuracy),
            sa_func.avg(Run.total_latency_ms),
        )
        .join(Run, Evaluation.run_id == Run.id)
        .join(Experiment, Run.experiment_id == Experiment.id)
        .filter(
            Experiment.dataset == experiment.dataset,
            Experiment.architecture == "single_agent",
            Experiment.status == "completed",
            Evaluation.accuracy.isnot(None),
        )
        .first()
    )

    baseline_accuracy: Optional[float] = None
    baseline_latency: Optional[float] = None
    if baseline_row and baseline_row[0] is not None:
        baseline_accuracy = float(baseline_row[0])
        baseline_latency = float(baseline_row[1] or 0)

    # Improvement per token
    improvement_per_token: Optional[float] = None
    if baseline_accuracy is not None and exp_tokens > 0:
        improvement_per_token = round(
            compute_improvement_per_token(exp_accuracy, baseline_accuracy, exp_tokens),
            8,
        )

    # Latency overhead %
    latency_overhead: Optional[float] = None
    if baseline_latency is not None and baseline_latency > 0:
        latency_overhead = round(
            compute_latency_overhead(exp_latency, baseline_latency), 2
        )

    # ------------------------------------------------------------------
    # 3. Convergence — from debate traces of the first run with traces
    # ------------------------------------------------------------------
    convergence_score_val: Optional[float] = None
    convergence_turns: list[ConvergenceTurn] = []

    first_run_with_traces = (
        db.query(Run)
        .filter(Run.experiment_id == exp_id)
        .join(DebateTrace, DebateTrace.run_id == Run.id)
        .order_by(Run.id)
        .first()
    )

    if first_run_with_traces is not None:
        traces = (
            db.query(DebateTrace.turn_number, DebateTrace.response)
            .filter(DebateTrace.run_id == first_run_with_traces.id)
            .order_by(DebateTrace.turn_number)
            .all()
        )
        if len(traces) >= 2:
            initial_text = traces[0][1] or ""
            final_text = traces[-1][1] or ""
            convergence_score_val = round(
                compute_convergence_score(initial_text, final_text), 4
            )
            convergence_turns = compute_convergence_turns(
                [(t[0], t[1] or "") for t in traces]
            )

    # ------------------------------------------------------------------
    # 4. Multi-run variance — across experiments with same config
    # ------------------------------------------------------------------
    # Each experiment's avg accuracy forms one data point
    multi_run_rows = (
        db.query(sa_func.avg(Evaluation.accuracy))
        .join(Run, Evaluation.run_id == Run.id)
        .join(Experiment, Run.experiment_id == Experiment.id)
        .filter(
            Experiment.architecture == experiment.architecture,
            Experiment.dataset == experiment.dataset,
            Experiment.model == experiment.model,
            Experiment.status == "completed",
            Evaluation.accuracy.isnot(None),
        )
        .group_by(Experiment.id)
        .all()
    )

    accuracy_scores = [float(row[0]) for row in multi_run_rows if row[0] is not None]

    accuracy_mean = round(statistics.mean(accuracy_scores), 4) if accuracy_scores else None
    accuracy_variance, accuracy_std = compute_variance_and_std(accuracy_scores)

    # Confidence interval
    confidence_interval: Optional[list[float]] = None
    if accuracy_mean is not None and accuracy_std is not None:
        confidence_interval = compute_confidence_interval(
            accuracy_mean, accuracy_std, len(accuracy_scores)
        )

    # ------------------------------------------------------------------
    # 5. Stability score
    # ------------------------------------------------------------------
    stability_score: Optional[float] = None
    if accuracy_mean is not None:
        var_for_stability = accuracy_variance if accuracy_variance is not None else 0.0
        stability_score = compute_stability_score(
            accuracy_mean, exp_hallucination, var_for_stability
        )

    # ------------------------------------------------------------------
    # Assemble
    # ------------------------------------------------------------------
    metrics = AdvancedMetrics(
        improvement_per_token=improvement_per_token,
        latency_overhead_percent=latency_overhead,
        convergence_score=convergence_score_val,
        accuracy_variance=accuracy_variance,
        accuracy_std=accuracy_std,
        accuracy_mean=accuracy_mean,
        confidence_interval=confidence_interval,
        stability_score=stability_score,
    )

    return metrics, convergence_turns
