from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_XZ_MAGIC = b"\xFD7zXZ\x00"

@register
class XzEngine(EngineBase):
    name = "xz"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_XZ_MAGIC):
            cand = Candidate(media_type="application/x-xz", extension="xz", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
