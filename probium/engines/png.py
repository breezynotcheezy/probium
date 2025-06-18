from __future__ import annotations
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

@register
class PNGEngine(EngineBase):
    name = "png"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_PNG_MAGIC):
            cand = Candidate(media_type="image/png", extension="png", confidence=0.99)
            return Result(candidates=[cand])
        return Result(candidates=[])
