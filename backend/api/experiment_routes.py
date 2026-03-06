"""Experiment API routes."""

import asyncio
import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from core.orchestrator import ExperimentRunner
from models.debate_trace import DebateTrace
from models.experiment import Experiment
from models.run import Run
from models.schemas import (
    ExperimentConfig,
    ExperimentStartResponse,
    ExperimentStatusResponse,
)
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
    completed_runs = (
        db.query(sa_func.count(Run.id))
        .filter(Run.experiment_id == exp_uuid)
        .scalar()
    ) or 0

    # Compute averages from completed runs
    avg_row = (
        db.query(
            sa_func.avg(Run.total_tokens),
            sa_func.avg(Run.total_latency_ms),
        )
        .filter(Run.experiment_id == exp_uuid)
        .first()
    )
    avg_tokens = round(float(avg_row[0] or 0), 2)
    avg_latency_ms = round(float(avg_row[1] or 0), 2)

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
        preview = t.response[:120] if t.response else ""
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
