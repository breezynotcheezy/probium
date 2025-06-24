from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class RubyEngine(EngineBase):
    name = "ruby"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first_line = text.splitlines()[0] if text else ""
        if first_line.startswith("#!") and "ruby" in first_line:
            cand = Candidate(
                media_type="text/x-ruby",
                extension="rb",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        head = text[:256]
        if "def " in head and "end" in text:
            cand = Candidate(
                media_type="text/x-ruby",
                extension="rb",
                confidence=score_tokens(0.05),
                breakdown={"token_ratio": 0.05},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
