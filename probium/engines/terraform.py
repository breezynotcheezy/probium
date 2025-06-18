from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class TerraformEngine(EngineBase):
    name = "terraform"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "terraform" in text and "required_version" in text:
            return Result(candidates=[Candidate(media_type="text/x-terraform", extension="tf", confidence=0.95)])
        if "resource" in text and "{" in text:
            return Result(candidates=[Candidate(media_type="text/x-terraform", extension="tf", confidence=0.8)])
        return Result(candidates=[])
