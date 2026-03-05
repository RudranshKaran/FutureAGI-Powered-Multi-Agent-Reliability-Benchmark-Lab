"""
Async LLM service — centralised wrapper around the OpenAI chat-completions API.

Every call returns a structured `LLMResponse` with:
  • response_text  — the model's reply
  • tokens_used    — total tokens (prompt + completion)
  • latency_ms     — wall-clock time for the API call
"""

import time
import logging

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from config.settings import settings
from models.schemas import LLMResponse

logger = logging.getLogger(__name__)

# Initialise the async client once at module level.
_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class LLMService:
    """Thin async wrapper around the OpenAI chat-completions endpoint."""

    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant.",
    ) -> LLMResponse:
        """Send *prompt* to the LLM and return a structured response.

        Parameters
        ----------
        prompt:
            The user message.
        system_prompt:
            An optional system-level instruction prepended to the conversation.

        Returns
        -------
        LLMResponse
            Contains `response_text`, `tokens_used`, and `latency_ms`.
        """
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        start = time.perf_counter()

        try:
            completion = await _client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
        except Exception:
            logger.exception("LLM API call failed")
            raise

        elapsed_ms = (time.perf_counter() - start) * 1000

        response_text = completion.choices[0].message.content or ""

        # Prefer provider-reported token count; fall back to rough estimate.
        if completion.usage is not None:
            tokens_used = completion.usage.total_tokens
        else:
            tokens_used = len(prompt.split()) + len(response_text.split())
            logger.warning("Token usage unavailable — using word-count estimate")

        return LLMResponse(
            response_text=response_text,
            tokens_used=tokens_used,
            latency_ms=round(elapsed_ms, 2),
        )
