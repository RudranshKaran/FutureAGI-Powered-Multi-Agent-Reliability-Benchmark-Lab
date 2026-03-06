"""Experiment API routes."""

import asyncio
import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from core.orchestrator import ExperimentRunner
from models.debate_trace import DebateTrace
from models.evaluation import Evaluation
from models.experiment import Experiment
from models.run import Run
from models.schemas import (
    ExperimentConfig,
    ExperimentResultsResponse,
    ExperimentStartResponse,
    ExperimentStatusResponse,
    ExperimentSummary,
    ArchitectureComparisonItem,
    TokenAccuracyPoint,
    RoundImprovement,
    PromptBreakdown,
    DebateTraceEntry,
)
from core.advanced_metrics import compute_advanced_metrics
from storage.database import SessionLocal, get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/experiments", tags=["experiments"])


def _run_experiment_background(config: ExperimentConfig) -> None:
    """Background task that runs the experiment with its own DB session."""
    db = SessionLocal()
    runner = ExperimentRunner()
    try:
        # BackgroundTasks runs in a thread without an event loop,
        # so we create one with asyncio.run().
        asyncio.run(runner.run_experiment(config, db))
    except Exception as exc:
        logger.exception("Background experiment failed: %s", exc)
    finally:
        db.close()


@router.post("/run", response_model=ExperimentStartResponse)
async def run_experiment(
    config: ExperimentConfig,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Launch an experiment in the background and return immediately."""

    # Validate architecture early so we fail fast
    from core.architectures import ARCHITECTURE_REGISTRY

    if config.architecture not in ARCHITECTURE_REGISTRY:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown architecture '{config.architecture}'. "
                f"Available: {list(ARCHITECTURE_REGISTRY.keys())}"
            ),
        )

    # Validate dataset early
    from core.datasets import load_dataset

    try:
        prompts = load_dataset(config.dataset)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Create the experiment record so we can return its ID immediately
    experiment = Experiment(
        architecture=config.architecture,
        rounds=config.rounds,
        model=config.model,
        dataset=config.dataset,
        status="pending",
        total_prompts=len(prompts),
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    experiment_id = str(experiment.id)

    # Launch the actual execution in a background thread
    background_tasks.add_task(_run_experiment_background, config)

    return ExperimentStartResponse(experiment_id=experiment_id)


@router.get("/{experiment_id}/status", response_model=ExperimentStatusResponse)
async def get_experiment_status(
    experiment_id: str,
    db: Session = Depends(get_db),
):
    """Return current execution status for a given experiment."""

    try:
        exp_uuid = UUID(experiment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid experiment ID format")

    experiment = db.query(Experiment).filter(Experiment.id == exp_uuid).first()
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    total_prompts = experiment.total_prompts or 0

    # Count completed runs (runs are only inserted after execution succeeds)
    completed_runs: int = (
        db.query(sa_func.count(Run.id))
        .filter(Run.experiment_id == exp_uuid)
        .scalar() or 0
    )

    # Compute averages from completed runs
    avg_row = (
        db.query(
            sa_func.avg(Run.total_tokens),
            sa_func.avg(Run.total_latency_ms),
        )
        .filter(Run.experiment_id == exp_uuid)
        .first()
    )
    avg_tokens = round(float(avg_row[0] or 0), 2) if avg_row else 0.0
    avg_latency_ms = round(float(avg_row[1] or 0), 2) if avg_row else 0.0

    progress_percentage = (
        round(completed_runs / total_prompts * 100, 1) if total_prompts > 0 else 0.0
    )

    # Build structured logs from DebateTraces (most recent 50)
    traces = (
        db.query(DebateTrace)
        .join(Run, DebateTrace.run_id == Run.id)
        .filter(Run.experiment_id == exp_uuid)
        .order_by(Run.id, DebateTrace.turn_number)
        .limit(50)
        .all()
    )

    logs: list[str] = []
    for t in traces:
        preview = (t.response or "")[:120]
        entry = (
            f"[Agent {t.agent_role} | Turn {t.turn_number} | "
            f"{t.latency_ms:.0f}ms | {t.tokens} tokens] {preview}"
        )
        logs.append(entry)

    return ExperimentStatusResponse(
        experiment_id=experiment_id,
        status=experiment.status,
        architecture=experiment.architecture,
        dataset=experiment.dataset,
        total_prompts=total_prompts,
        completed_runs=completed_runs,
        progress_percentage=progress_percentage,
        avg_tokens=avg_tokens,
        avg_latency_ms=avg_latency_ms,
        logs=logs,
    )


@router.get("/{experiment_id}/results", response_model=ExperimentResultsResponse)
async def get_experiment_results(
    experiment_id: str,
    db: Session = Depends(get_db),
):
    """Return full analytics data for a completed experiment."""

    try:
        exp_uuid = UUID(experiment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid experiment ID format")

    experiment = db.query(Experiment).filter(Experiment.id == exp_uuid).first()
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    if experiment.status != "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Experiment is '{experiment.status}', results are only available for completed experiments",
        )

    # ---- Summary metrics ----
    summary_row = (
        db.query(
            sa_func.avg(Evaluation.accuracy),
            sa_func.avg(Evaluation.hallucination),
            sa_func.avg(Run.total_tokens),
            sa_func.avg(Run.total_latency_ms),
        )
        .join(Run, Evaluation.run_id == Run.id)
        .filter(Run.experiment_id == exp_uuid)
        .first()
    )

    if summary_row:
        summary = ExperimentSummary(
            avg_accuracy=round(float(summary_row[0]), 4) if summary_row[0] is not None else None,
            avg_hallucination=round(float(summary_row[1]), 4) if summary_row[1] is not None else None,
            avg_tokens=round(float(summary_row[2] or 0), 2),
            avg_latency_ms=round(float(summary_row[3] or 0), 2),
        )
    else:
        summary = ExperimentSummary()

    # ---- Architecture comparison (all completed experiments on same dataset) ----
    arch_rows = (
        db.query(
            Experiment.architecture,
            sa_func.avg(Evaluation.accuracy),
        )
        .join(Run, Run.experiment_id == Experiment.id)
        .join(Evaluation, Evaluation.run_id == Run.id)
        .filter(
            Experiment.dataset == experiment.dataset,
            Experiment.status == "completed",
            Evaluation.accuracy.isnot(None),
        )
        .group_by(Experiment.architecture)
        .all()
    )

    architecture_comparison = [
        ArchitectureComparisonItem(
            architecture=row[0],
            accuracy=round(float(row[1]), 4),
        )
        for row in arch_rows
    ]

    # ---- Token vs Accuracy scatter points ----
    ta_rows = (
        db.query(Run.total_tokens, Evaluation.accuracy)
        .join(Evaluation, Evaluation.run_id == Run.id)
        .filter(
            Run.experiment_id == exp_uuid,
            Evaluation.accuracy.isnot(None),
        )
        .all()
    )

    token_accuracy_points = [
        TokenAccuracyPoint(tokens=int(row[0]), accuracy=round(float(row[1]), 4))
        for row in ta_rows
    ]

    # ---- Round improvement (same dataset + architecture, grouped by rounds) ----
    round_rows = (
        db.query(
            Experiment.rounds,
            sa_func.avg(Evaluation.accuracy),
        )
        .join(Run, Run.experiment_id == Experiment.id)
        .join(Evaluation, Evaluation.run_id == Run.id)
        .filter(
            Experiment.dataset == experiment.dataset,
            Experiment.architecture == experiment.architecture,
            Experiment.status == "completed",
            Evaluation.accuracy.isnot(None),
        )
        .group_by(Experiment.rounds)
        .order_by(Experiment.rounds)
        .all()
    )

    round_improvement = [
        RoundImprovement(rounds=int(row[0]), accuracy=round(float(row[1]), 4))
        for row in round_rows
    ]

    # ---- Prompt breakdown with debate traces ----
    runs = (
        db.query(Run)
        .filter(Run.experiment_id == exp_uuid)
        .order_by(Run.id)
        .all()
    )

    prompt_breakdown: list[PromptBreakdown] = []
    for run in runs:
        eval_row = (
            db.query(Evaluation)
            .filter(Evaluation.run_id == run.id)
            .first()
        )

        traces = (
            db.query(DebateTrace)
            .filter(DebateTrace.run_id == run.id)
            .order_by(DebateTrace.turn_number)
            .all()
        )

        prompt_breakdown.append(
            PromptBreakdown(
                prompt=run.prompt,
                final_output=run.final_output,
                accuracy=eval_row.accuracy if eval_row and eval_row.accuracy is not None else None,
                tokens=run.total_tokens,
                latency_ms=run.total_latency_ms,
                debate_traces=[
                    DebateTraceEntry(
                        agent_role=t.agent_role,
                        turn_number=t.turn_number,
                        response=t.response,
                        tokens=t.tokens,
                        latency_ms=t.latency_ms,
                    )
                    for t in traces
                ],
            )
        )

    # ---- Advanced metrics ----
    advanced_metrics, convergence_turns = compute_advanced_metrics(db, experiment)

    return ExperimentResultsResponse(
        experiment_id=experiment_id,
        architecture=experiment.architecture,
        dataset=experiment.dataset,
        rounds=experiment.rounds,
        summary=summary,
        architecture_comparison=architecture_comparison,
        token_accuracy_points=token_accuracy_points,
        round_improvement=round_improvement,
        prompt_breakdown=prompt_breakdown,
        advanced_metrics=advanced_metrics,
        convergence_turns=convergence_turns,
    )
