from __future__ import annotations

import json
import re
from ..scoring import score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

@register
class JSONEngine(EngineBase):
    name = "json"
    #Identifier for this engine

    #Estimated cost to run this engine (used for prioritization or budgeting)
    cost = 0.05

    _TOKEN_RE = re.compile(r'[{}\[\]":,]')

    def _make_result(self, conf: float, token_ratio: float, partial: bool = False) -> Result:
        """Helper to build a :class:`Result` object."""

        cand = Candidate(
            media_type="application/json",
            extension="json",
            confidence=conf,
            breakdown={"token_ratio": round(token_ratio, 3), "partial": partial},
        )
        return Result(candidates=[cand])

    def _find_json_fragment(self, text: str) -> str | None:
        """Return the first valid JSON snippet inside ``text`` if present."""

        decoder = json.JSONDecoder()
        for match in re.finditer(r"[\{\[]", text):
            start = match.start()
            try:
                obj, idx = decoder.raw_decode(text[start:])
                end = start + idx
                return text[start:end]
            except Exception:
                continue
        return None

    def sniff(self, payload: bytes) -> Result:
        """Detect JSON by analyzing structure rather than magic bytes."""

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])

        text = text.strip()
        if not text:
            return Result(candidates=[])

        token_count = len(self._TOKEN_RE.findall(text))
        token_ratio = token_count / max(len(text), 1)

        try:
            json.loads(text)
            return self._make_result(score_tokens(1.0), token_ratio)
        except Exception:
            pass

        frag = self._find_json_fragment(text)
        if frag is not None:
            try:
                json.loads(frag)
                conf = score_tokens(min(0.9, token_ratio))
                return self._make_result(conf, token_ratio, partial=True)
            except Exception:
                pass

        if token_ratio > 0.3 and ":" in text:
            conf = score_tokens(min(token_ratio, 0.8))
            return self._make_result(conf, token_ratio, partial=True)

        return Result(candidates=[])
