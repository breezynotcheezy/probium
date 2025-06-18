from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class PerlEngine(EngineBase):
    name = "perl"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first_line = text.splitlines()[0] if text else ""
        if first_line.startswith("#!") and "perl" in first_line:
            return Result(candidates=[Candidate(media_type="text/x-perl", extension="pl", confidence=0.99)])
        if "use strict" in text and "my $" in text:
            return Result(candidates=[Candidate(media_type="text/x-perl", extension="pl", confidence=0.8)])
        return Result(candidates=[])
