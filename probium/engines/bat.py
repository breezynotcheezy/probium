from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class BATEngine(EngineBase):
    name = "bat"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        first_line = payload.splitlines()[:1]
        if first_line:
            line = first_line[0].lower()
            if line.startswith((b"@echo", b"echo", b"rem", b"::")):
                cand = Candidate(media_type="application/x-bat", extension="bat", confidence=0.9)
                return Result(candidates=[cand])
        return Result(candidates=[])
