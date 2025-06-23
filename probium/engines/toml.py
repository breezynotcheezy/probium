from __future__ import annotations

from ..models import Candidate, Result
from .base import MagicEngine
from ..registry import register
import logging

logger = logging.getLogger(__name__)

@register
class TomlEngine(MagicEngine):
    name = "toml"
    cost = 0.05
    magic_hint = "toml"

    def sniff(self, payload: bytes) -> Result:
        res = self._probe_magic(payload)
        if res:
            return res

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "=" in text and "[" in text and "]" in text and "\n" in text:
            if "[" in text.splitlines()[0]:
                return Result(candidates=[Candidate(media_type="application/toml", extension="toml", confidence=0.9)])
        return Result(candidates=[])
