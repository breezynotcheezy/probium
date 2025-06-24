from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_RAR_MAGIC = b"Rar!"

@register
class RarEngine(EngineBase):
    name = "rar"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_RAR_MAGIC):
            cand = Candidate(
                media_type="application/vnd.rar",
                extension="rar",
                confidence=score_magic(len(_RAR_MAGIC)),
                breakdown={"magic_len": float(len(_RAR_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
