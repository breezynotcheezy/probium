from __future__ import annotations
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

try:
    from magika import Magika
except Exception as exc:  # pragma: no cover - optional dependency
    Magika = None  # type: ignore


@register
class MagikaEngine(EngineBase):
    """Engine backed by the Google Magika library."""

    name = "magika"
    cost = 0.05
    opt_in_only = True

    def __init__(self) -> None:
        super().__init__()
        if Magika is None:
            raise RuntimeError("Google Magika library is required for this engine")
        self._magika = Magika()

    def sniff(self, payload: bytes) -> Result:
        res = self._magika.identify_bytes(payload)
        info = res.prediction.output
        cand = Candidate(
            media_type=info.mime_type,
            extension=info.extensions[0] if info.extensions else None,
            confidence=float(res.prediction.score),
        )
        return Result(candidates=[cand])
