from __future__ import annotations
import string
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class TextEngine(EngineBase):
    name = "text"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        sample = payload[:512]
        try:
            text = sample.decode("utf-8")
        except UnicodeDecodeError:
            return Result(candidates=[])
        printable = set(string.printable)
        printable_count = sum(1 for c in text if c in printable or c in "\n\r\t")
        ratio = printable_count / max(len(text), 1)
        if ratio > 0.95 and "<" not in text and ">" not in text:
            conf = round(ratio, 2)
            cand = Candidate(media_type="text/plain", extension="txt", confidence=conf)
            return Result(candidates=[cand])
        return Result(candidates=[])
