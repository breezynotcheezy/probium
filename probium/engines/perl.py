from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class PerlEngine(EngineBase):
    name = "perl"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first_line = text.splitlines()[0] if text else ""
        if first_line.startswith("#!") and "perl" in first_line:
            cand = Candidate(
                media_type="text/x-perl",
                extension="pl",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        if "use strict" in text and "my $" in text:
            cand = Candidate(
                media_type="text/x-perl",
                extension="pl",
                confidence=score_tokens(0.05),
                breakdown={"token_ratio": 0.05},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
