from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_SQLITE_MAGIC = b"SQLite format 3\x00"

@register
class SQLiteEngine(EngineBase):
    name = "sqlite"
    cost = 0.1

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_SQLITE_MAGIC):
            cand = Candidate(
                media_type="application/vnd.sqlite3",
                extension="sqlite",
                confidence=score_magic(len(_SQLITE_MAGIC)),
                breakdown={"magic_len": float(len(_SQLITE_MAGIC))},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
