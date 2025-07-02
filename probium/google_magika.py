from __future__ import annotations
from pathlib import Path
from typing import Any

from .core import _detect_file
from .models import Result
import importlib


def magika_available() -> bool:
    """Return ``True`` if the optional ``magika`` package can be imported."""
    try:
        importlib.import_module("magika")
    except Exception:
        return False
    return True


def require_magika() -> None:
    """Raise ``RuntimeError`` if the ``magika`` package is missing."""
    if not magika_available():
        raise RuntimeError(
            "Google Magika library is required. Install with `pip install magika`."
        )


def detect_magika(source: str | Path | bytes, *, cap_bytes: int | None = None) -> Result:
    """Detect file type using only the Google Magika engine."""
    require_magika()
    return _detect_file(source, engine="magika", cap_bytes=cap_bytes)
