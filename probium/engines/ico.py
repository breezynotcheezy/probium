from __future__ import annotations

from ..scoring import score_magic, score_tokens
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
            cand = Candidate(
                media_type="image/x-icon",
                extension="ico",
                confidence=score_magic(len(_ICO_MAGIC)),
                breakdown={"magic_len": float(len(_ICO_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
