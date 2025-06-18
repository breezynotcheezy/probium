from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_FLAC_MAGIC = b"fLaC"

@register
class FlacEngine(EngineBase):
    name = "flac"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_FLAC_MAGIC):
            cand = Candidate(media_type="audio/flac", extension="flac", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
