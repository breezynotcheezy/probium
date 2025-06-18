from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class RustEngine(EngineBase):
    name = "rust"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "fn main()" in text and "println!" in text:
            return Result(candidates=[Candidate(media_type="text/x-rust", extension="rs", confidence=0.95)])
        return Result(candidates=[])
