from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class JSONEngine(EngineBase):
    name = "json"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        window = payload.lstrip()[:1]
        if window in (b"{", b"["):
            cand = Candidate(media_type="application/json", extension="json", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
