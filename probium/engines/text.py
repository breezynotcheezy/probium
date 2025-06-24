from __future__ import annotations
import string
from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class TextEngine(EngineBase):
    name = "text"
    cost = 1.0

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
            conf = score_tokens(ratio)
            cand = Candidate(
                media_type="text/plain",
                extension="txt",
                confidence=conf,
                breakdown={"token_ratio": ratio},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
