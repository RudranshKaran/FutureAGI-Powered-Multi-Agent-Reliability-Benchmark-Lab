"""Abstract base class for all agent reasoning architectures."""

from abc import ABC, abstractmethod

from core.llm_service import LLMService
from models.schemas import ArchitectureResult


class BaseArchitecture(ABC):
    """Every architecture receives an LLMService and implements `execute`."""

    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    @abstractmethod
    async def execute(self, prompt: str) -> ArchitectureResult:
        """Run the architecture on *prompt* and return a structured result."""
        ...
