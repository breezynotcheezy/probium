from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class ImageEngine(EngineBase):
    name = "image"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        cand = []
        if payload.startswith(b"\xff\xd8\xff"):
            cand.append(Candidate(media_type="image/jpeg", extension="jpg", confidence=0.99))
        elif payload.startswith(b"GIF87a") or payload.startswith(b"GIF89a"):
            cand.append(Candidate(media_type="image/gif", extension="gif", confidence=0.99))
        return Result(candidates=cand)
