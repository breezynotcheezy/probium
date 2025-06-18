from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class ClojureEngine(EngineBase):
    name = "clojure"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.startswith("(ns") or "(defn" in text:
            return Result(candidates=[Candidate(media_type="text/x-clojure", extension="clj", confidence=0.9)])
        return Result(candidates=[])
