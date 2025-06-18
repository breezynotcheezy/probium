from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class YAMLEngine(EngineBase):
    name = "yaml"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if ':' in text and '\n' in text and not text.lstrip().startswith('{'):
            if '-' in text or ':' in text.splitlines()[0]:
                return Result(candidates=[Candidate(media_type="text/x-yaml", extension="yaml", confidence=0.7)])
        return Result(candidates=[])
