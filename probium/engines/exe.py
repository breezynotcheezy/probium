from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_MZ = b"MZ"

@register
class EXEEngine(EngineBase):
    name = "exe"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_MZ):
            cand = Candidate(
                media_type="application/vnd.microsoft.portable-executable",
                extension="exe",
                confidence=score_magic(len(_MZ)),
                breakdown={"magic_len": float(len(_MZ))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
