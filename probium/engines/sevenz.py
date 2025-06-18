from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_SEVENZ_MAGIC = b"7z\xBC\xAF\x27\x1C"

@register
class SevenZEngine(EngineBase):
    name = "7z"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_SEVENZ_MAGIC):
            cand = Candidate(media_type="application/x-7z-compressed", extension="7z", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
