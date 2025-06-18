from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class ScalaEngine(EngineBase):
    name = "scala"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "object " in text and "extends App" in text:
            return Result(candidates=[Candidate(media_type="text/x-scala", extension="scala", confidence=0.95)])
        return Result(candidates=[])
