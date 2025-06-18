from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class MarkdownEngine(EngineBase):
    name = "markdown"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.startswith("# ") or "\n# " in text:
            return Result(candidates=[Candidate(media_type="text/markdown", extension="md", confidence=0.9)])
        if "[" in text and "](" in text:
            return Result(candidates=[Candidate(media_type="text/markdown", extension="md", confidence=0.7)])
        return Result(candidates=[])
