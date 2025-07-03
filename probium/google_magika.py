from __future__ import annotations
from pathlib import Path
from typing import Any
import os

from .models import Result
import importlib


def magika_available() -> bool:
    """Return ``True`` if the optional ``magika`` package can be imported."""
    try:
        importlib.import_module("magika")
    except Exception:
        return False
    return True


def magika_env_only() -> bool:
    """Return ``True`` if the environment forces Magika-only detection."""
    return os.getenv("PROBIUM_MAGIKA_ONLY", "").lower() in {"1", "true", "yes"}


def require_magika() -> None:
    """Raise ``RuntimeError`` if the ``magika`` package is missing."""
    if not magika_available():
        raise RuntimeError(
            "Google Magika library is required. Install with `pip install magika`."
        )


def detect_magika(source: str | Path | bytes, *, cap_bytes: int | None = None) -> Result:
    """Detect file type using only the Google Magika engine."""
    require_magika()
    from .core import _detect_file
    return _detect_file(source, engine="magika", cap_bytes=cap_bytes)
