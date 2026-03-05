"""FutureAGI evaluator — sends run outputs for reliability scoring."""

import logging
from typing import Optional

import httpx

from config.settings import settings
from models.schemas import EvaluationResult

logger = logging.getLogger(__name__)


class FutureAGIEvaluator:
    """Async client that sends prompt/response pairs to the FutureAGI
    evaluation API and returns structured reliability metrics."""

    def __init__(self) -> None:
        self._api_url = settings.FUTUREAGI_API_URL
        self._api_key = settings.FUTUREAGI_API_KEY
        self._client = httpx.AsyncClient(timeout=10.0)

    async def evaluate(
        self, prompt: str, response: str
    ) -> Optional[EvaluationResult]:
        """Evaluate a single prompt/response pair.

        Returns an ``EvaluationResult`` on success or ``None`` if the
        API call fails for any reason (timeout, HTTP error, bad payload).
        """
        try:
            http_response = await self._client.post(
                self._api_url,
                json={"prompt": prompt, "response": response},
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
            )
            http_response.raise_for_status()

            data = http_response.json()
            result = EvaluationResult(
                accuracy=data.get("accuracy"),
                hallucination=data.get("hallucination"),
                coherence=data.get("coherence"),
                safety=data.get("safety"),
            )

            logger.info(
                "[FutureAGI] Run evaluated | accuracy=%s hallucination=%s coherence=%s safety=%s",
                result.accuracy,
                result.hallucination,
                result.coherence,
                result.safety,
            )
            return result

        except httpx.TimeoutException:
            logger.warning("[FutureAGI] Evaluation timed out")
            return None
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "[FutureAGI] Evaluation failed — HTTP %s: %s",
                exc.response.status_code,
                exc.response.text[:200],
            )
            return None
        except Exception as exc:
            logger.warning("[FutureAGI] Evaluation failed — %s", exc)
            return None

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()
