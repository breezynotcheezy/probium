from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class TomlEngine(EngineBase):
    name = "toml"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "=" in text and "[" in text and "]" in text and "\n" in text:
            if "[" in text.splitlines()[0]:
                return Result(candidates=[Candidate(media_type="application/toml", extension="toml", confidence=0.9)])
        return Result(candidates=[])
