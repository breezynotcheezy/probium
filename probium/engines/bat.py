from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class BATEngine(EngineBase):
    name = "bat"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        first_line = payload.splitlines()[:1]
        if first_line:
            line = first_line[0].lower()
            if line.startswith((b"@echo", b"echo", b"rem", b"::")):
                cand = Candidate(
                    media_type="application/x-bat",
                    extension="bat",
                    confidence=score_tokens(1.0),
                    breakdown={"token_ratio": 1.0},
                )
                return Result(candidates=[cand])
        return Result(candidates=[])
