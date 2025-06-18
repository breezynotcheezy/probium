from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class PHPEngine(EngineBase):
    name = "php"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.lstrip().startswith("<?php"):
            return Result(candidates=[Candidate(media_type="text/x-php", extension="php", confidence=0.95)])
        if "$" in text and "function" in text and "<?" in text:
            return Result(candidates=[Candidate(media_type="text/x-php", extension="php", confidence=0.8)])
        return Result(candidates=[])
