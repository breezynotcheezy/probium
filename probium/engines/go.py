from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class GoEngine(EngineBase):
    name = "go"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.startswith("package ") and "func main()" in text:
            cand = Candidate(
                media_type="text/x-go",
                extension="go",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        if "package main" in text and "fmt." in text:
            cand = Candidate(
                media_type="text/x-go",
                extension="go",
                confidence=score_tokens(0.05),
                breakdown={"token_ratio": 0.05},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
