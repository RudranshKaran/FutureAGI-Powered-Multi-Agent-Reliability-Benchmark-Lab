"""Dataset loader — reads prompt lists from local JSON files."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Project root: two levels up from this file (backend/core/datasets.py → project root)
_DATASETS_DIR = Path(__file__).resolve().parents[2] / "data" / "datasets"


def load_dataset(name: str) -> list[str]:
    """Load a dataset by name and return a list of prompt strings.

    Parameters
    ----------
    name:
        Dataset identifier (e.g. ``"arithmetic"``).  Resolves to
        ``data/datasets/{name}.json`` relative to the project root.

    Returns
    -------
    list[str]
        The prompt strings contained in the dataset file.

    Raises
    ------
    ValueError
        If the dataset file does not exist or contains invalid data.
    """

    dataset_path = _DATASETS_DIR / f"{name}.json"

    if not dataset_path.is_file():
        available = [p.stem for p in _DATASETS_DIR.glob("*.json")] if _DATASETS_DIR.is_dir() else []
        raise ValueError(
            f"Dataset '{name}' not found at {dataset_path}. "
            f"Available datasets: {available}"
        )

    try:
        data = json.loads(dataset_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Dataset '{name}' contains invalid JSON: {exc}") from exc

    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        raise ValueError(
            f"Dataset '{name}' must be a JSON array of strings."
        )

    logger.info("Loaded dataset '%s' with %d prompts", name, len(data))
    return data
