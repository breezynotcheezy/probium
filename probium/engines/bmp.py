from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_BMP_MAGIC = b"BM"

@register
class BMPEngine(EngineBase):
    name = "bmp"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_BMP_MAGIC):
            cand = Candidate(
                media_type="image/bmp",
                extension="bmp",
                confidence=score_magic(len(_BMP_MAGIC)),
                breakdown={"magic_len": float(len(_BMP_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
