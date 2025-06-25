from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class JSONEngine(EngineBase):
    name = "json"
    #Identifier for this engine

    #Estimated cost to run this engine (used for prioritization or budgeting)
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
         #Strip leading whitespace and look at the first non-space byte
        window = payload.lstrip()[:1]
         #If it starts with '{' or '[', it might be JSON
        if window in (b"{", b"["):
            #Create a high-confidence candidate for JSON
            cand = Candidate(
                media_type="application/json",
                extension="json",
                confidence=score_tokens(1.0),  #Token-based confidence score
                breakdown={"token_ratio": 1.0},  #Optional debug info
            )
            return Result(candidates=[cand])
        return Result(candidates=[])#Return empty if there was no match
