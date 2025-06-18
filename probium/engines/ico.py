from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_ICO_MAGIC = b"\x00\x00\x01\x00"

@register
class IcoEngine(EngineBase):
    name = "ico"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_ICO_MAGIC):
            cand = Candidate(media_type="image/x-icon", extension="ico", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
