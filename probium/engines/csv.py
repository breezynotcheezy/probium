from __future__ import annotations
import csv
import io
import logging
import mimetypes
import re
import hashlib
from functools import lru_cache
from typing import Optional

try:  # optional dependency
    import chardet  # type: ignore
except Exception:  # pragma: no cover - fallback when chardet isn't installed
    chardet = None

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

    # Configurable constants
    DELIMS = ",;\t|"
    MIN_ROWS = 3
    SAMPLE_LINES = 20
    SAMPLE_SIZE = 4096  # bytes for initial analysis
    CHUNK_SIZE = 8192  # bytes for streaming
    TOKEN_RATIO_THRESHOLD = 0.01
    CONSISTENCY_THRESHOLD = 0.5

    # Confidence levels
    MAGIC_CONFIDENCE = 0.9
    HIGH_CONFIDENCE = 0.8
    MEDIUM_CONFIDENCE = 0.5
    HEADER_BOOST = 0.1

    _TOKEN_RE = re.compile(r"[,\t;|]")
    BOM_UTF8 = b'\xef\xbb\xbf'
    BOM_UTF16_LE = b'\xff\xfe'
    BOM_UTF16_BE = b'\xfe\xff'
    MAGIC_PATTERNS = [b'sep=', b'#', b'"', b',']  # Extended magic patterns

    def detect_encoding(self, payload: bytes) -> str:
        """Detect the encoding of the payload using BOMs or chardet."""
        if payload.startswith(self.BOM_UTF8):
            logger.debug("Detected UTF-8 BOM")
            return 'utf-8-sig'
        elif payload.startswith(self.BOM_UTF16_LE):
            logger.debug("Detected UTF-16 LE BOM")
            return 'utf-16-le'
        elif payload.startswith(self.BOM_UTF16_BE):
            logger.debug("Detected UTF-16 BE BOM")
            return 'utf-16-be'
        else:
            if chardet is not None:
                try:
                    enc = chardet.detect(payload[:self.SAMPLE_SIZE]).get('encoding')
                    if enc:
                        logger.debug("Detected encoding via chardet: %s", enc)
                        return enc
                except Exception:
                    logger.debug("Chardet failed, falling back to UTF-8")
            return 'utf-8'

    def detect_delimiter(self, sample: str) -> Optional[str]:
        """Fallback method to detect the delimiter if csv.Sniffer fails."""
        candidates = list(self.DELIMS)
        scores = {}
        for d in candidates:
            counts = [ln.count(d) for ln in sample.splitlines() if ln.strip()]
            if counts and len(set(counts)) == 1 and counts[0] > 0:
                scores[d] = counts[0]
        if scores:
            delim = max(scores, key=scores.get)
            logger.debug("Detected delimiter: %s", delim)
            return delim
        logger.debug("No consistent delimiter found")
        return None

    @lru_cache(maxsize=128)
    def _analyze_sample(self, payload_hash: str, text_sample: str) -> tuple:
        """Analyze a sample of text, cached by payload hash."""
        lines = text_sample.splitlines()[:self.SAMPLE_LINES]
        sample = '\n'.join(lines)
        if not sample.strip():
            logger.debug("Sample is empty after stripping")
            return None, None, [], 0.0, 0.0

        # Detect delimiter
        try:
            dialect = csv.Sniffer().sniff(sample, self.DELIMS)
            logger.debug("csv.Sniffer detected delimiter: %s", dialect.delimiter)
        except Exception:
            delim = self.detect_delimiter(sample)
            if not delim:
                logger.debug("Fallback delimiter detection failed")
                return None, None, [], 0.0, 0.0
            dialect = csv.excel()
            dialect.delimiter = delim

        # Parse rows
        try:
            reader = csv.reader(io.StringIO(sample), dialect)
            rows = [row for row in reader if row]
        except Exception as e:
            logger.debug("CSV parsing failed: %s", e)
            return None, None, [], 0.0, 0.0

        if len(rows) < self.MIN_ROWS:
            logger.debug("Too few rows: %d < %d", len(rows), self.MIN_ROWS)
            return None, None, [], 0.0, 0.0

        # Analyze column consistency
        column_counts = [len(r) for r in rows]
        if not column_counts:
            return None, None, [], 0.0, 0.0
        most_common_count = max(set(column_counts), key=column_counts.count)
        consistency_ratio = column_counts.count(most_common_count) / len(rows)
        token_count = sum(len(self._TOKEN_RE.findall(ln)) for ln in lines)
        total_chars = sum(len(ln) for ln in lines)
        token_ratio = token_count / total_chars if total_chars > 0 else 0

        try:
            has_header = csv.Sniffer().has_header(sample)
        except Exception:
            logger.debug("csv.Sniffer.has_header failed")
            has_header = False

        return dialect, has_header, rows, consistency_ratio, token_ratio

    def _make_result(
        self,
        conf: float,
        token_ratio: float,
        *,
        partial: bool = False,
        magic_len: Optional[int] = None,
        consistency_ratio: float = 1.0,
    ) -> Result:
        """Create a Result object with detailed breakdown."""
        breakdown = {
            "token<|control630|>": round(token_ratio, 3),
            "partial": partial,
            "consistency_ratio": round(consistency_ratio, 3),
        }
        if magic_len is not None:
            breakdown["magic_len"] = magic_len
        cand = Candidate(
            media_type="text/csv",
            extension="csv",
            confidence=conf,
            breakdown=breakdown,
        )
        return Result(candidates=[cand])

    def sniff(self, payload: bytes) -> Result:
        """Detect if the payload is a CSV file with improved robustness and performance."""
        # Check libmagic first
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload[:self.SAMPLE_SIZE])
                logger.debug("libmagic MIME: %s", mime)
                if mime and "csv" in mime.lower():
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "csv"
                    cand = Candidate(
                        media_type=mime,
                        extension=ext,
                        confidence=self.MAGIC_CONFIDENCE,
                        breakdown={"libmagic": True},
                    )
                    return Result(candidates=[cand])
            except Exception as e:
                logger.warning("libmagic failed: %s", e)

        # Sample and decode
        payload_sample = payload[:self.SAMPLE_SIZE]
        encoding = self.detect_encoding(payload_sample)
        try:
            text_sample = payload_sample.decode(encoding, errors='replace')
        except Exception as e:
            logger.debug("Decoding failed with %s: %s", encoding, e)
            return Result(candidates=[])

        # Check for binary data
        if any(ord(c) < 32 and ord(c) not in (9, 10, 13) for c in text_sample):
            logger.debug("Binary data detected in sample")
            return Result(candidates=[])

        # Check magic patterns
        magic_len = None
        for m in self.MAGIC_PATTERNS:
            if payload_sample.startswith(m):
                magic_len = len(m)
                logger.debug("Magic pattern matched: %s", m)
                break

        # Analyze sample with caching
        payload_hash = hashlib.md5(payload_sample).hexdigest()
        dialect, has_header, rows, consistency_ratio, token_ratio = self._analyze_sample(payload_hash, text_sample)
        if not rows:
            return Result(candidates=[])

        if consistency_ratio < self.CONSISTENCY_THRESHOLD:
            logger.debug("Consistency ratio too low: %.2f", consistency_ratio)
            return Result(candidates=[])

        # Calculate confidence
        base_conf = self.MEDIUM_CONFIDENCE
        if consistency_ratio > 0.8:
            base_conf = self.HIGH_CONFIDENCE
        elif consistency_ratio > self.CONSISTENCY_THRESHOLD:
            base_conf += 0.1
        if has_header:
            base_conf += self.HEADER_BOOST
            logger.debug("Header detected, boosting confidence")
        if magic_len:
            base_conf = max(base_conf, self.MAGIC_CONFIDENCE)
        if token_ratio > self.TOKEN_RATIO_THRESHOLD:
            base_conf += 0.1
            logger.debug("Token ratio sufficient: %.3f", token_ratio)

        conf = min(base_conf, 1.0)
        logger.debug("Final confidence: %.2f", conf)

        partial = False
        return self._make_result(
            conf,
            token_ratio,
            partial=partial,
            magic_len=magic_len,
            consistency_ratio=consistency_ratio
        )

