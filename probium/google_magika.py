from __future__ import annotations
from pathlib import Path
from typing import Any

from .core import _detect_file
from .models import Result


def detect_magika(source: str | Path | bytes, *, cap_bytes: int | None = None) -> Result:
    """Detect file type using only the Google Magika engine."""
    return _detect_file(source, engine="magika", cap_bytes=cap_bytes)
