from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register

@register
class OctetEngine(EngineBase):
    name = "fallback-engine"
    cost = 100.0

    def sniff(self, payload: bytes) -> Result:
        return Result(
            candidates=[
                Candidate(
                    media_type="*UNSAFE* / *NO ENGINE*",
                    confidence=0.0,
                )
            ]
        )
