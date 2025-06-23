from __future__ import annotations

from ..models import Candidate, Result
from .base import MagicEngine
from ..registry import register
import logging

logger = logging.getLogger(__name__)

@register
class SwiftEngine(MagicEngine):
    name = "swift"
    cost = 0.05
    magic_hint = "swift"

    def sniff(self, payload: bytes) -> Result:
        res = self._probe_magic(payload)
        if res:
            return res

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "import Swift" in text or "import Foundation" in text:
            return Result(candidates=[Candidate(media_type="text/x-swift", extension="swift", confidence=0.95)])
        if "func " in text and "let " in text:
            return Result(candidates=[Candidate(media_type="text/x-swift", extension="swift", confidence=0.8)])
        return Result(candidates=[])
