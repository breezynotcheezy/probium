from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
from ..magicdb import match_magic
import logging

logger = logging.getLogger(__name__)


@register
class SwiftEngine(EngineBase):
    name = "swift"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        cand = match_magic(payload)
        if cand:
            return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "import Swift" in text or "import Foundation" in text:
            return Result(candidates=[Candidate(media_type="text/x-swift", extension="swift", confidence=0.95)])
        if "func " in text and "let " in text:
            return Result(candidates=[Candidate(media_type="text/x-swift", extension="swift", confidence=0.8)])
        return Result(candidates=[])
