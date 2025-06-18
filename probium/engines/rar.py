from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_RAR_MAGIC = b"Rar!"

@register
class RarEngine(EngineBase):
    name = "rar"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_RAR_MAGIC):
            cand = Candidate(media_type="application/vnd.rar", extension="rar", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
