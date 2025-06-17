from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_ID3_MAGIC = b"ID3"

@register
class MP3Engine(EngineBase):
    name = "mp3"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_ID3_MAGIC) or payload[:2] == b"\xff\xfb":
            cand = Candidate(media_type="audio/mpeg", extension="mp3", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
