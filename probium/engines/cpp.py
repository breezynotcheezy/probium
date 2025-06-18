from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class CppEngine(EngineBase):
    name = "cpp"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        head = text[:512]
        if "#include <iostream>" in head or "std::" in text:
            return Result(candidates=[Candidate(media_type="text/x-c++", extension="cpp", confidence=0.9)])
        return Result(candidates=[])
