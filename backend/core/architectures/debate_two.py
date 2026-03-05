"""TwoAgentDebate architecture — Agent A proposes, Agent B critiques, Agent A revises."""

from core.architectures.base import BaseArchitecture
from models.schemas import ArchitectureResult, ArchitectureStep


class TwoAgentDebate(BaseArchitecture):
    """Two-agent debate with configurable rounds.

    Flow (per round):
        1. Agent A → initial answer (round 1) or revision (rounds 2+)
        2. Agent B → critique of Agent A's latest answer
        3. Agent A → revision incorporating the critique

    The final output is Agent A's last revision.
    """

    def __init__(self, llm_service, rounds: int = 1):
        super().__init__(llm_service)
        self.rounds = max(1, rounds)

    async def execute(self, prompt: str) -> ArchitectureResult:
        steps: list[ArchitectureStep] = []
        total_tokens = 0
        total_latency = 0.0
        turn = 0

        # --- Turn 1: Agent A initial answer ---
        turn += 1
        agent_a_resp = await self.llm.generate(
            prompt,
            system_prompt="You are a proposer. Provide a clear, well-reasoned answer to the question.",
        )
        steps.append(
            ArchitectureStep(
                agent="agent_a",
                turn=turn,
                response=agent_a_resp.response_text,
                tokens=agent_a_resp.tokens_used,
                latency_ms=agent_a_resp.latency_ms,
            )
        )
        total_tokens += agent_a_resp.tokens_used
        total_latency += agent_a_resp.latency_ms

        current_answer = agent_a_resp.response_text

        for _round in range(self.rounds):
            # --- Agent B critiques ---
            turn += 1
            critique_prompt = (
                f"Original question: {prompt}\n\n"
                f"Proposed answer:\n{current_answer}\n\n"
                "Provide a detailed critique of the above answer. "
                "Identify any errors, logical gaps, or areas for improvement."
            )
            agent_b_resp = await self.llm.generate(
                critique_prompt,
                system_prompt="You are a critic. Your job is to rigorously evaluate and critique answers.",
            )
            steps.append(
                ArchitectureStep(
                    agent="agent_b",
                    turn=turn,
                    response=agent_b_resp.response_text,
                    tokens=agent_b_resp.tokens_used,
                    latency_ms=agent_b_resp.latency_ms,
                )
            )
            total_tokens += agent_b_resp.tokens_used
            total_latency += agent_b_resp.latency_ms

            # --- Agent A revises ---
            turn += 1
            revision_prompt = (
                f"Original question: {prompt}\n\n"
                f"Your previous answer:\n{current_answer}\n\n"
                f"Critique received:\n{agent_b_resp.response_text}\n\n"
                "Revise your answer to address the critique. "
                "Produce an improved, well-reasoned response."
            )
            revision_resp = await self.llm.generate(
                revision_prompt,
                system_prompt="You are a proposer. Revise your answer based on the critique provided.",
            )
            steps.append(
                ArchitectureStep(
                    agent="agent_a",
                    turn=turn,
                    response=revision_resp.response_text,
                    tokens=revision_resp.tokens_used,
                    latency_ms=revision_resp.latency_ms,
                )
            )
            total_tokens += revision_resp.tokens_used
            total_latency += revision_resp.latency_ms

            current_answer = revision_resp.response_text

        return ArchitectureResult(
            final_output=current_answer,
            total_tokens=total_tokens,
            total_latency_ms=round(total_latency, 2),
            steps=steps,
        )
