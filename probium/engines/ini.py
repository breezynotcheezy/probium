from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class INIEngine(EngineBase):
    name = "ini"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.lstrip().startswith("[") and "]" in text and "=" in text:
            return Result(candidates=[Candidate(media_type="text/x-ini", extension="ini", confidence=0.9)])
        return Result(candidates=[])
