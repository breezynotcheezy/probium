from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class RubyEngine(EngineBase):
    name = "ruby"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first_line = text.splitlines()[0] if text else ""
        if first_line.startswith("#!") and "ruby" in first_line:
            return Result(candidates=[Candidate(media_type="text/x-ruby", extension="rb", confidence=0.99)])
        head = text[:256]
        if "def " in head and "end" in text:
            return Result(candidates=[Candidate(media_type="text/x-ruby", extension="rb", confidence=0.8)])
        return Result(candidates=[])
