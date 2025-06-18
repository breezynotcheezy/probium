from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class LuaEngine(EngineBase):
    name = "lua"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.lstrip().startswith("#!/usr/bin/env lua"):
            return Result(candidates=[Candidate(media_type="text/x-lua", extension="lua", confidence=0.99)])
        if "function" in text and "end" in text:
            return Result(candidates=[Candidate(media_type="text/x-lua", extension="lua", confidence=0.8)])
        return Result(candidates=[])
