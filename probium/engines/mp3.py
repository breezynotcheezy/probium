from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register

_ID3_MAGIC = b"ID3"

@register
class MP3Engine(EngineBase):
    name = "mp3"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_ID3_MAGIC) or payload[:2] == b"\xff\xfb":
            cand = Candidate(
                media_type="audio/mpeg",
                extension="mp3",
                confidence=score_magic(len(_ID3_MAGIC)),
                breakdown={"magic_len": float(len(_ID3_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
