from __future__ import annotations

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
            return Result(candidates=[Candidate(media_type="text/x-haskell", extension="hs", confidence=0.95)])
        if "import" in text and "::" in text:
            return Result(candidates=[Candidate(media_type="text/x-haskell", extension="hs", confidence=0.8)])
        return Result(candidates=[])
