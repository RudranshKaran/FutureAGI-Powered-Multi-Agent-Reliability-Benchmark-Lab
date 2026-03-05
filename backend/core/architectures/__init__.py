"""
Architecture registry — maps string identifiers to architecture classes.

Usage:
    from core.architectures import ARCHITECTURE_REGISTRY

    cls = ARCHITECTURE_REGISTRY["single_agent"]
    arch = cls(llm_service=llm)
    result = await arch.execute(prompt)
"""

from core.architectures.single_agent import SingleAgent
from core.architectures.debate_two import TwoAgentDebate
from core.architectures.self_refine import SelfRefinement

ARCHITECTURE_REGISTRY: dict[str, type] = {
    "single_agent": SingleAgent,
    "two_agent_debate": TwoAgentDebate,
    "self_refinement": SelfRefinement,
}

__all__ = [
    "ARCHITECTURE_REGISTRY",
    "SingleAgent",
    "TwoAgentDebate",
    "SelfRefinement",
]
