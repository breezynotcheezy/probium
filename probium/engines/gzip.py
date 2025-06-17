from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_GZIP_MAGIC = b"\x1f\x8b"

@register
class GzipEngine(EngineBase):
    name = "gzip"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_GZIP_MAGIC):
            cand = Candidate(media_type="application/gzip", extension="gz", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
