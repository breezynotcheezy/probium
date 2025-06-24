from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class MakefileEngine(EngineBase):
    name = "makefile"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first = text.splitlines()[0] if text else ""
        if ":" in first and ("$(" in text or "\n\t" in text):
            cand = Candidate(
                media_type="text/x-makefile",
                extension="mk",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
