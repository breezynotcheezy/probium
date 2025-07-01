from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register

_GZIP_MAGIC = b"\x1f\x8b"

@register
class GzipEngine(EngineBase):
    name = "gzip"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_GZIP_MAGIC):
            cand = Candidate(
                media_type="application/gzip",
                extension="gz",
                confidence=score_magic(len(_GZIP_MAGIC)),
                breakdown={"magic_len": float(len(_GZIP_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
