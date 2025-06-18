from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class JavaEngine(EngineBase):
    name = "java"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        head = text[:512]
        if "public class" in head and "static void main" in text:
            return Result(candidates=[Candidate(media_type="text/x-java-source", extension="java", confidence=0.95)])
        if head.lstrip().startswith("import java"):
            return Result(candidates=[Candidate(media_type="text/x-java-source", extension="java", confidence=0.8)])
        return Result(candidates=[])
