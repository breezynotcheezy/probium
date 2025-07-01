from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class WAVEngine(EngineBase):
    name = "wav"
    cost = 0.1
    _MAGIC = b"RIFF"
    _FMT = b"WAVE"

    def sniff(self, payload: bytes) -> Result:
        if len(payload) >= 12 and payload[:4] == self._MAGIC and payload[8:12] == self._FMT:
            cand = Candidate(
                media_type="audio/wav",
                extension="wav",
                confidence=score_magic(len(self._MAGIC)),
                breakdown={"magic_len": float(len(self._MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
