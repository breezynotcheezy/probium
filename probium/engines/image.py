from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register

@register
class ImageEngine(EngineBase):
    name = "image"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        cand = []
        if payload.startswith(b"\xff\xd8\xff"):
            cand.append(
                Candidate(
                    media_type="image/jpeg",
                    extension="jpg",
                    confidence=score_magic(3),
                    breakdown={"magic_len": 3.0},
                )
            )
        elif payload.startswith(b"GIF87a") or payload.startswith(b"GIF89a"):
            cand.append(
                Candidate(
                    media_type="image/gif",
                    extension="gif",
                    confidence=score_magic(6),
                    breakdown={"magic_len": 6.0},
                )
            )
        return Result(candidates=cand)
