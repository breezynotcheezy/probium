from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class CSharpEngine(EngineBase):
    name = "csharp"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "using System" in text and "static void Main" in text:
            return Result(candidates=[Candidate(media_type="text/x-csharp", extension="cs", confidence=0.95)])
        if "namespace" in text and "class" in text:
            return Result(candidates=[Candidate(media_type="text/x-csharp", extension="cs", confidence=0.8)])
        return Result(candidates=[])
