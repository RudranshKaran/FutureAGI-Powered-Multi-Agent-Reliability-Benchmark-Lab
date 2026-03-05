"""SingleAgent architecture — one LLM call, no debate or refinement."""

from core.architectures.base import BaseArchitecture
from models.schemas import ArchitectureResult, ArchitectureStep


class SingleAgent(BaseArchitecture):
    """Baseline: send the prompt to the LLM once and return the answer."""

    async def execute(self, prompt: str) -> ArchitectureResult:
        result = await self.llm.generate(prompt)

        step = ArchitectureStep(
            agent="single_agent",
            turn=1,
            response=result.response_text,
            tokens=result.tokens_used,
            latency_ms=result.latency_ms,
        )

        return ArchitectureResult(
            final_output=result.response_text,
            total_tokens=result.tokens_used,
            total_latency_ms=result.latency_ms,
            steps=[step],
        )
