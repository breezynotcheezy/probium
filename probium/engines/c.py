from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class CEngine(EngineBase):
    name = "c"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        head = text[:256]
        if "#include" in head and "int main" in text:
            return Result(candidates=[Candidate(media_type="text/x-c", extension="c", confidence=0.9)])
        return Result(candidates=[])
