from __future__ import annotations

from ..models import Candidate, Result
from .base import MagicEngine
from ..registry import register
import logging

logger = logging.getLogger(__name__)

@register
class CppEngine(MagicEngine):
    name = "cpp"
    cost = 0.05
    magic_hint = "c++"

    def sniff(self, payload: bytes) -> Result:
        res = self._probe_magic(payload)
        if res:
            return res

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        head = text[:512]
        if "#include <iostream>" in head or "std::" in text:
            return Result(candidates=[Candidate(media_type="text/x-c++", extension="cpp", confidence=0.9)])
        return Result(candidates=[])
