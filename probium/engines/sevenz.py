from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_SEVENZ_MAGIC = b"7z\xBC\xAF\x27\x1C"

@register
class SevenZEngine(EngineBase):
    name = "7z"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_SEVENZ_MAGIC):
            cand = Candidate(
                media_type="application/x-7z-compressed",
                extension="7z",
                confidence=score_magic(len(_SEVENZ_MAGIC)),
                breakdown={"magic_len": float(len(_SEVENZ_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
