from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_FLAC_MAGIC = b"fLaC"

@register
class FlacEngine(EngineBase):
    name = "flac"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_FLAC_MAGIC):
            cand = Candidate(
                media_type="audio/flac",
                extension="flac",
                confidence=score_magic(len(_FLAC_MAGIC)),
                breakdown={"magic_len": float(len(_FLAC_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
