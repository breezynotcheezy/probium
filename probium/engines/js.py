from __future__ import annotations

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
            return Result(candidates=[Candidate(media_type="application/javascript", extension="js", confidence=0.9)])
        return Result(candidates=[])
