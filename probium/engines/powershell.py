from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
from ..magicdb import match_magic
import logging

logger = logging.getLogger(__name__)


@register
class PowerShellEngine(EngineBase):
    name = "powershell"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        cand = match_magic(payload)
        if cand:
            return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.lstrip().startswith("#requires") or "Write-Host" in text:
            return Result(candidates=[Candidate(media_type="text/x-powershell", extension="ps1", confidence=0.9)])
        return Result(candidates=[])
