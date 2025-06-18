from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class DockerfileEngine(EngineBase):
    name = "dockerfile"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.startswith("FROM ") or "\nFROM " in text:
            return Result(candidates=[Candidate(media_type="text/x-dockerfile", extension="dockerfile", confidence=0.95)])
        if "RUN" in text and "CMD" in text:
            return Result(candidates=[Candidate(media_type="text/x-dockerfile", extension="dockerfile", confidence=0.8)])
        return Result(candidates=[])
