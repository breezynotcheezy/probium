from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class KotlinEngine(EngineBase):
    name = "kotlin"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "fun main" in text and "println(" in text:
            return Result(candidates=[Candidate(media_type="text/x-kotlin", extension="kt", confidence=0.95)])
        if "class " in text and "val " in text:
            return Result(candidates=[Candidate(media_type="text/x-kotlin", extension="kt", confidence=0.8)])
        return Result(candidates=[])
