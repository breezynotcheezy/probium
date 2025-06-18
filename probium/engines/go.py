from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class GoEngine(EngineBase):
    name = "go"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.startswith("package ") and "func main()" in text:
            return Result(candidates=[Candidate(media_type="text/x-go", extension="go", confidence=0.95)])
        if "package main" in text and "fmt." in text:
            return Result(candidates=[Candidate(media_type="text/x-go", extension="go", confidence=0.8)])
        return Result(candidates=[])
