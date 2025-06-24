from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_XZ_MAGIC = b"\xFD7zXZ\x00"

@register
class XzEngine(EngineBase):
    name = "xz"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_XZ_MAGIC):
            cand = Candidate(
                media_type="application/x-xz",
                extension="xz",
                confidence=score_magic(len(_XZ_MAGIC)),
                breakdown={"magic_len": float(len(_XZ_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
