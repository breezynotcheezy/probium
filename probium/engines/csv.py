from __future__ import annotations

import csv
import io
import logging
import mimetypes
import re

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()


@register
class CSVEngine(EngineBase):
    name = "csv"
    cost = 0.05

    # Possible delimiters to check for in CSV files
    DELIMS = ",;\t|"

    MIN_ROWS = 3
    MIN_COLS = 2
    SAMPLE_LINES = 20

    _TOKEN_RE = re.compile(r"[,\t;|]")
    _MAGIC = [b"\xEF\xBB\xBF", b"sep="]

    def _make_result(
        self,
        conf: float,
        token_ratio: float,
        *,
        partial: bool = False,
        magic_len: int | None = None,
    ) -> Result:
        """Build a :class:`Result` with common metadata."""

        breakdown = {"token_ratio": round(token_ratio, 3), "partial": partial}
        if magic_len is not None:
            breakdown["magic_len"] = float(magic_len)

        cand = Candidate(
            media_type="text/csv",
            extension="csv",
            confidence=conf,
            breakdown=breakdown,
        )
        return Result(candidates=[cand])

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover - rare
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "csv" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "csv"
                    cand = Candidate(
                        media_type=mime,
                        extension=ext,
                        confidence=score_tokens(1.0),
                        breakdown={"token_ratio": 1.0, "libmagic": True},
                    )
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])

        stripped = text.lstrip()
        magic_hit = None
        for m in self._MAGIC:
            if stripped.startswith(m.decode("latin1")):
                magic_hit = m
                break

        text = text.strip()
        if not text:
            return Result(candidates=[])

        lines = text.splitlines()
        sample = "\n".join(lines[: self.SAMPLE_LINES])

        try:
            dialect = csv.Sniffer().sniff(sample, self.DELIMS)
        except Exception:
            return Result(candidates=[])

        delim = dialect.delimiter
        token_count = len(self._TOKEN_RE.findall(sample))
        token_ratio = token_count / max(len(sample), 1)

        delim_hits = sum(delim in ln for ln in lines[: self.SAMPLE_LINES])
        if delim_hits < self.MIN_ROWS:
            return Result(candidates=[])

        try:
            reader = csv.reader(io.StringIO(sample), dialect)
            rows = [row for row in reader if row]
        except Exception:
            return Result(candidates=[])

        if len(rows) < self.MIN_ROWS:
            return Result(candidates=[])

        column_counts = {len(r) for r in rows}
        same_len = len(column_counts) == 1 and next(iter(column_counts)) >= self.MIN_COLS

        has_header = csv.Sniffer().has_header(sample)

        if same_len:
            conf_base = 0.9 if has_header else 0.7
        else:
            conf_base = 0.6

        conf = score_tokens(conf_base)
        if magic_hit:
            conf = max(conf, score_magic(len(magic_hit)))

        return self._make_result(conf, token_ratio, partial=not same_len, magic_len=len(magic_hit) if magic_hit else None)
