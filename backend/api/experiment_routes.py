"""Experiment API routes."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.orchestrator import ExperimentRunner
from models.schemas import ExperimentConfig, ExperimentResult
from storage.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("/run", response_model=ExperimentResult)
async def run_experiment(
    config: ExperimentConfig,
    db: Session = Depends(get_db),
):
    """Launch an experiment: iterate over dataset prompts, execute the
    selected architecture, persist results, and return aggregate metrics."""

    runner = ExperimentRunner()

    try:
        result = await runner.run_experiment(config, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Experiment failed")
        raise HTTPException(
            status_code=500, detail=f"Experiment execution failed: {exc}"
        )

    return result
