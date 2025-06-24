from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class JavaScriptEngine(EngineBase):
    name = "js"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        head = text[:256]
        if "function " in head or "console.log" in head or "=>" in head:
            cand = Candidate(
                media_type="application/javascript",
                extension="js",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
