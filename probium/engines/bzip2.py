from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_BZ_MAGIC = b"BZh"

@register
class Bzip2Engine(EngineBase):
    name = "bzip2"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_BZ_MAGIC):
            cand = Candidate(
                media_type="application/x-bzip",
                extension="bz2",
                confidence=score_magic(len(_BZ_MAGIC)),
                breakdown={"magic_len": float(len(_BZ_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
