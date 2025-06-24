from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_OGG_MAGIC = b"OggS"

@register
class OggEngine(EngineBase):
    name = "ogg"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_OGG_MAGIC):
            cand = Candidate(
                media_type="application/ogg",
                extension="ogg",
                confidence=score_magic(len(_OGG_MAGIC)),
                breakdown={"magic_len": float(len(_OGG_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
