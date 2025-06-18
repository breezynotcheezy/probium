from __future__ import annotations
import filetype
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class MagicEngine(EngineBase):
    """Generic detector using filetype library."""
    name = "magic"
    cost = 10.0

    def sniff(self, payload: bytes) -> Result:
        kind = filetype.guess(payload)
        if not kind:
            return Result(candidates=[])
        cand = Candidate(media_type=kind.mime, extension=kind.extension, confidence=0.9)
        return Result(candidates=[cand])
