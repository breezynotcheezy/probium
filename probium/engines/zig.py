from __future__ import annotations

from ..models import Candidate, Result
from .base import MagicEngine
from ..registry import register
import logging

logger = logging.getLogger(__name__)

@register
class ZigEngine(MagicEngine):
    name = "zig"
    cost = 0.05
    magic_hint = "zig"

    def sniff(self, payload: bytes) -> Result:
        res = self._probe_magic(payload)
        if res:
            return res

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "pub fn main" in text and "std.debug" in text:
            return Result(candidates=[Candidate(media_type="text/x-zig", extension="zig", confidence=0.9)])
        return Result(candidates=[])
