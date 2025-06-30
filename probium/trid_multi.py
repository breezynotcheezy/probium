from __future__ import annotations
from pathlib import Path
from typing import Any, Iterable
from .core import _detect_file as detect
from .models import Result


def detect_with_trid(
    source: str | Path | bytes,
    *,
    cap_bytes: int | None = 4096,
    engine_order: Iterable[str] | None = None,
    only: Iterable[str] | None = None,
    extensions: Iterable[str] | None = None,
    cache: bool = True,
) -> dict[str, Result]:
    """Run built-in detection and TRiD engine if available.

    Returns a mapping with keys ``probium`` and ``trid``.
    """
    base = detect(
        source,
        cap_bytes=cap_bytes,
        engine_order=engine_order,
        only=only,
        extensions=extensions,
        cache=cache,
    )
    trid_res = detect(
        source,
        engine="trid",
        cap_bytes=cap_bytes,
        engine_order=engine_order,
        only=None if only is None else [e for e in only if e == "trid"],
        extensions=extensions,
        cache=cache,
    )
    return {"probium": base, "trid": trid_res}
