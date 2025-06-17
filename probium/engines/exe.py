from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_MZ = b"MZ"

@register
class EXEEngine(EngineBase):
    name = "exe"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_MZ):
            cand = Candidate(media_type="application/vnd.microsoft.portable-executable", extension="exe", confidence=0.99)
            return Result(candidates=[cand])
        return Result(candidates=[])
