from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class JavaEngine(EngineBase):
    name = "java"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        head = text[:512]
        if "public class" in head and "static void main" in text:
            cand = Candidate(
                media_type="text/x-java-source",
                extension="java",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        if head.lstrip().startswith("import java"):
            cand = Candidate(
                media_type="text/x-java-source",
                extension="java",
                confidence=score_tokens(0.05),
                breakdown={"token_ratio": 0.05},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
