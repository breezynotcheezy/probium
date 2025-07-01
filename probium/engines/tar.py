from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_TAR_MAGIC = b"ustar"

@register
class TAREngine(EngineBase):
    name = "tar"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if len(payload) > 262 and payload[257:262] == _TAR_MAGIC:
            cand = Candidate(
                media_type="application/x-tar",
                extension="tar",
                confidence=score_magic(len(_TAR_MAGIC)),
                breakdown={"magic_len": float(len(_TAR_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
