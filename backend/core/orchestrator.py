"""Experiment orchestrator — coordinates dataset → architecture → persistence."""

import logging
from statistics import mean
from typing import Optional

from sqlalchemy.orm import Session

from core.architectures import ARCHITECTURE_REGISTRY
from core.architectures.debate_two import TwoAgentDebate
from core.datasets import load_dataset
from core.evaluator import FutureAGIEvaluator
from core.llm_service import LLMService
from models.debate_trace import DebateTrace
from models.evaluation import Evaluation
from models.experiment import Experiment
from models.run import Run
from models.schemas import ExperimentConfig, ExperimentResult

logger = logging.getLogger(__name__)


class ExperimentRunner:
    """Runs a full experiment: iterates over dataset prompts, executes the
    selected architecture, persists results and debate traces, and computes
    derived metrics."""

    async def run_experiment(
        self, config: ExperimentConfig, db: Session
    ) -> ExperimentResult:
        """Execute an end-to-end experiment and return a summary.

        Parameters
        ----------
        config:
            The experiment configuration (architecture, dataset, model, etc.).
        db:
            An active SQLAlchemy session used for persistence.

        Returns
        -------
        ExperimentResult
            Aggregate metrics for this experiment.
        """

        # -- 1. Validate architecture -----------------------------------
        arch_cls = ARCHITECTURE_REGISTRY.get(config.architecture)
        if arch_cls is None:
            raise ValueError(
                f"Unknown architecture '{config.architecture}'. "
                f"Available: {list(ARCHITECTURE_REGISTRY.keys())}"
            )

        # -- 2. Load dataset --------------------------------------------
        prompts = load_dataset(config.dataset)

        # -- 3. Find existing pending experiment or create a new one ----
        #    When launched via the API, the route pre-creates the experiment
        #    with status="pending" so its ID can be returned immediately.
        experiment = (
            db.query(Experiment)
            .filter(
                Experiment.architecture == config.architecture,
                Experiment.dataset == config.dataset,
                Experiment.model == config.model,
                Experiment.status == "pending",
            )
            .order_by(Experiment.created_at.desc())
            .first()
        )

        if experiment is None:
            experiment = Experiment(
                architecture=config.architecture,
                rounds=config.rounds,
                model=config.model,
                dataset=config.dataset,
                total_prompts=len(prompts),
            )
            db.add(experiment)
            db.flush()

        experiment.status = "running"  # type: ignore[assignment]
        experiment.total_prompts = len(prompts)  # type: ignore[assignment]
        db.commit()  # make status visible to polling

        # -- 4. Instantiate LLM + architecture --------------------------
        llm = LLMService(model=config.model, temperature=config.temperature)

        if arch_cls is TwoAgentDebate:
            architecture = arch_cls(llm_service=llm, rounds=config.rounds)
        else:
            architecture = arch_cls(llm_service=llm)

        # -- 5. Instantiate evaluator ----------------------------------
        evaluator = FutureAGIEvaluator()

        # -- 6. Execute each prompt ------------------------------------
        total_prompts = len(prompts)
        all_tokens: list[int] = []
        all_latencies: list[float] = []
        all_accuracy: list[float] = []
        all_hallucination: list[float] = []
        all_coherence: list[float] = []
        all_safety: list[float] = []

        try:
            for idx, prompt in enumerate(prompts, start=1):
                result = await architecture.execute(prompt)

                # Persist Run
                run = Run(
                    experiment_id=experiment.id,
                    prompt=prompt,
                    final_output=result.final_output,
                    total_tokens=result.total_tokens,
                    total_latency_ms=result.total_latency_ms,
                )
                db.add(run)
                db.flush()  # populate run.id

                # Persist DebateTraces
                for step in result.steps:
                    trace = DebateTrace(
                        run_id=run.id,
                        agent_role=step.agent,
                        turn_number=step.turn,
                        response=step.response,
                        tokens=step.tokens,
                        latency_ms=step.latency_ms,
                    )
                    db.add(trace)

                # Evaluate via FutureAGI
                eval_result = await evaluator.evaluate(
                    prompt=prompt, response=result.final_output
                )

                if eval_result is not None:
                    evaluation = Evaluation(
                        run_id=run.id,
                        accuracy=eval_result.accuracy,
                        hallucination=eval_result.hallucination,
                        coherence=eval_result.coherence,
                        safety=eval_result.safety,
                    )
                    db.add(evaluation)

                    if eval_result.accuracy is not None:
                        all_accuracy.append(eval_result.accuracy)
                    if eval_result.hallucination is not None:
                        all_hallucination.append(eval_result.hallucination)
                    if eval_result.coherence is not None:
                        all_coherence.append(eval_result.coherence)
                    if eval_result.safety is not None:
                        all_safety.append(eval_result.safety)
                else:
                    logger.warning(
                        "[FutureAGI] Evaluation failed for run %s", run.id
                    )

                all_tokens.append(result.total_tokens)
                all_latencies.append(result.total_latency_ms)

                # Commit after each run so the status endpoint reflects progress
                db.commit()

                logger.info(
                    "[ExperimentRunner] Run %d/%d completed | tokens=%d latency=%.0fms",
                    idx,
                    total_prompts,
                    result.total_tokens,
                    result.total_latency_ms,
                )
        except Exception:
            experiment.status = "failed"  # type: ignore[assignment]
            db.commit()
            raise
        finally:
            await evaluator.close()

        # -- 7. Mark experiment completed ------------------------------
        experiment.status = "completed"  # type: ignore[assignment]
        db.commit()

        # -- 8. Compute derived metrics --------------------------------
        avg_tokens = round(mean(all_tokens), 2) if all_tokens else 0.0
        avg_latency_ms = round(mean(all_latencies), 2) if all_latencies else 0.0

        avg_accuracy: Optional[float] = (
            round(mean(all_accuracy), 4) if all_accuracy else None
        )
        avg_hallucination: Optional[float] = (
            round(mean(all_hallucination), 4) if all_hallucination else None
        )
        avg_coherence: Optional[float] = (
            round(mean(all_coherence), 4) if all_coherence else None
        )
        avg_safety: Optional[float] = (
            round(mean(all_safety), 4) if all_safety else None
        )

        logger.info(
            "[ExperimentRunner] Experiment %s complete | runs=%d avg_tokens=%.1f avg_latency=%.1fms",
            experiment.id,
            total_prompts,
            avg_tokens,
            avg_latency_ms,
        )

        return ExperimentResult(
            experiment_id=str(experiment.id),
            total_runs=total_prompts,
            avg_tokens=avg_tokens,
            avg_latency_ms=avg_latency_ms,
            avg_accuracy=avg_accuracy,
            avg_hallucination=avg_hallucination,
            avg_coherence=avg_coherence,
            avg_safety=avg_safety,
        )
