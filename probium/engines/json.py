from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class JSONEngine(EngineBase):
    name = "json"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        window = payload.lstrip()[:1]
        if window in (b"{", b"["):
            cand = Candidate(
                media_type="application/json",
                extension="json",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
