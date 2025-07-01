from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register

@register
class MP4Engine(EngineBase):
    name = "mp4"
    cost = 0.2
    _MAGIC = b"ftyp"

    def sniff(self, payload: bytes) -> Result:
        if len(payload) >= 12 and payload[4:8] == self._MAGIC:
            cand = Candidate(
                media_type="video/mp4",
                extension="mp4",
                confidence=score_magic(len(self._MAGIC)),
                breakdown={"magic_len": float(len(self._MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
