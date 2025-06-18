from __future__ import annotations
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_HTML_MAGIC = b"<html"

@register
class HTMLEngine(EngineBase):
    name = "html"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        window = payload[:32].lower()
        if _HTML_MAGIC in window:
            cand = Candidate(media_type="text/html", extension="html", confidence=0.95)
            return Result(candidates=[cand])
        return Result(candidates=[])
