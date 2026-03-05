"""SelfRefinement architecture — initial answer → self-critique → refined answer."""

from core.architectures.base import BaseArchitecture
from models.schemas import ArchitectureResult, ArchitectureStep


class SelfRefinement(BaseArchitecture):
    """Single-agent iterative self-refinement.

    Flow:
        1. Generate an initial answer.
        2. Critique the initial answer.
        3. Produce a refined answer incorporating the critique.
    """

    async def execute(self, prompt: str) -> ArchitectureResult:
        steps: list[ArchitectureStep] = []
        total_tokens = 0
        total_latency = 0.0

        # --- Step 1: Initial answer ---
        initial = await self.llm.generate(
            prompt,
            system_prompt="You are a helpful assistant. Provide a clear answer.",
        )
        steps.append(
            ArchitectureStep(
                agent="self_refine",
                turn=1,
                response=initial.response_text,
                tokens=initial.tokens_used,
                latency_ms=initial.latency_ms,
            )
        )
        total_tokens += initial.tokens_used
        total_latency += initial.latency_ms

        # --- Step 2: Self-critique ---
        critique_prompt = (
            f"Original question: {prompt}\n\n"
            f"Your previous answer:\n{initial.response_text}\n\n"
            "Critique your own answer. Identify any errors, weaknesses, "
            "logical gaps, or areas that could be improved."
        )
        critique = await self.llm.generate(
            critique_prompt,
            system_prompt="You are a self-critical assistant reviewing your own work.",
        )
        steps.append(
            ArchitectureStep(
                agent="self_refine",
                turn=2,
                response=critique.response_text,
                tokens=critique.tokens_used,
                latency_ms=critique.latency_ms,
            )
        )
        total_tokens += critique.tokens_used
        total_latency += critique.latency_ms

        # --- Step 3: Refined answer ---
        refine_prompt = (
            f"Original question: {prompt}\n\n"
            f"Your previous answer:\n{initial.response_text}\n\n"
            f"Self-critique:\n{critique.response_text}\n\n"
            "Produce an improved answer that addresses every point raised "
            "in the self-critique."
        )
        refined = await self.llm.generate(
            refine_prompt,
            system_prompt="You are a helpful assistant. Improve your answer based on your self-critique.",
        )
        steps.append(
            ArchitectureStep(
                agent="self_refine",
                turn=3,
                response=refined.response_text,
                tokens=refined.tokens_used,
                latency_ms=refined.latency_ms,
            )
        )
        total_tokens += refined.tokens_used
        total_latency += refined.latency_ms

        return ArchitectureResult(
            final_output=refined.response_text,
            total_tokens=total_tokens,
            total_latency_ms=round(total_latency, 2),
            steps=steps,
        )
