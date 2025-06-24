from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class HaskellEngine(EngineBase):
    name = "haskell"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "module" in text and "where" in text:
            cand = Candidate(
                media_type="text/x-haskell",
                extension="hs",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        if "import" in text and "::" in text:
            cand = Candidate(
                media_type="text/x-haskell",
                extension="hs",
                confidence=score_tokens(0.05),
                breakdown={"token_ratio": 0.05},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
