from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class MP4Engine(EngineBase):
    name = "mp4"
    cost = 0.2
    _MAGIC = b"ftyp"

    def sniff(self, payload: bytes) -> Result:
        if len(payload) >= 12 and payload[4:8] == self._MAGIC:
            cand = Candidate(media_type="video/mp4", extension="mp4", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
