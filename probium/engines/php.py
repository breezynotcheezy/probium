from __future__ import annotations

from ..models import Candidate, Result
from .base import MagicEngine
from ..registry import register
import logging

logger = logging.getLogger(__name__)

@register
class PHPEngine(MagicEngine):
    name = "php"
    cost = 0.05
    magic_hint = "php"

    def sniff(self, payload: bytes) -> Result:
        res = self._probe_magic(payload)
        if res:
            return res

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.lstrip().startswith("<?php"):
            return Result(candidates=[Candidate(media_type="text/x-php", extension="php", confidence=0.95)])
        if "$" in text and "function" in text and "<?" in text:
            return Result(candidates=[Candidate(media_type="text/x-php", extension="php", confidence=0.8)])
        return Result(candidates=[])
