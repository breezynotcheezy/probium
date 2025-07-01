from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register

_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

@register
class PNGEngine(EngineBase):
    name = "png"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_PNG_MAGIC):
            cand = Candidate(
                media_type="image/png",
                extension="png",
                confidence=score_magic(len(_PNG_MAGIC)),
                breakdown={"magic_len": float(len(_PNG_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
