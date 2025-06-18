from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class ElixirEngine(EngineBase):
    name = "elixir"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "defmodule" in text and "do" in text:
            return Result(candidates=[Candidate(media_type="text/x-elixir", extension="ex", confidence=0.9)])
        return Result(candidates=[])
