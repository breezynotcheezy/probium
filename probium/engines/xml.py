from __future__ import annotations
import logging
import mimetypes
import re
import xml.etree.ElementTree as ET
from functools import lru_cache

try:
    import chardet  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    chardet = None

from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()


@register
class XMLEngine(EngineBase):
    """Heuristic XML detection with multiple analysis layers."""

    name = "xml"
    cost = 0.05

    SAMPLE_SIZE = 4096
    TOKEN_RATIO_THRESHOLD = 0.05

    BOM_UTF8 = b"\xEF\xBB\xBF"
    BOM_UTF16_LE = b"\xFF\xFE"
    BOM_UTF16_BE = b"\xFE\xFF"
    MAGIC_PATTERNS = [BOM_UTF8, BOM_UTF16_LE, BOM_UTF16_BE, b"<?xml"]

    DECL_RE = re.compile(r"<\?xml[^>]*>")
    DOCTYPE_RE = re.compile(r"<!DOCTYPE[^>]+>", re.I)
    TOKEN_RE = re.compile(r"[<>]")
    OPEN_TAG_RE = re.compile(r"<[^/!?][^>]*>")
    CLOSE_TAG_RE = re.compile(r"</[^>]+>")

    def detect_encoding(self, payload: bytes) -> str:
        if payload.startswith(self.BOM_UTF8):
            return "utf-8-sig"
        if payload.startswith(self.BOM_UTF16_LE):
            return "utf-16-le"
        if payload.startswith(self.BOM_UTF16_BE):
            return "utf-16-be"
        if chardet is not None:
            try:
                enc = chardet.detect(payload[: self.SAMPLE_SIZE]).get("encoding")
                if enc:
                    return enc
            except Exception:
                pass
        return "utf-8"

    def _make_result(self, conf: float, breakdown: dict[str, float]) -> Result:
        cand = Candidate(
            media_type="application/xml",
            extension="xml",
            confidence=conf,
            breakdown=breakdown,
        )
        return Result(candidates=[cand])

    @lru_cache(maxsize=64)
    def _parse_snippet(self, snippet: str) -> bool:
        """Attempt to parse a snippet of XML, cached by content."""
        try:
            ET.fromstring(snippet)
            return True
        except Exception:
            try:
                ET.fromstring(f"<root>{snippet}</root>")
                return True
            except Exception:
                return False

    def sniff(self, payload: bytes) -> Result:
        """Return a detection result for the given payload."""
        cand=[]
        # 1. libmagic check
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover - rare
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "xml" in mime:
                    if not (b'<!DOCTYPE html' in payload or b'<!DOCTYPE HTML' in payload or b'<html>' in payload or b'<HTML' in payload):
                        ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "xml"
                        cand = Candidate(
                            media_type=mime,
                            extension=ext,
                            confidence=score_tokens(1.0),
                            breakdown={"libmagic": True},
                        )
                        return Result(candidates=[cand])

        encoding = self.detect_encoding(payload)
        try:
            text = payload.decode(encoding, errors="replace")
        except Exception:
            return Result(candidates=[])

        window = text[: self.SAMPLE_SIZE]
        breakdown: dict[str, float] = {}
        confidence = 0.0

        token_ratio = len(self.TOKEN_RE.findall(window)) / max(len(window), 1)
        if token_ratio < self.TOKEN_RATIO_THRESHOLD / 2:
            return Result(candidates=[])

        # 2. XML declaration / BOM
        if window.lstrip().startswith("<?xml"):
            confidence = max(confidence, score_magic(5))
            breakdown["xml_decl"] = 1.0
        for magic in (self.BOM_UTF8, self.BOM_UTF16_LE, self.BOM_UTF16_BE):
            if payload.startswith(magic):
                confidence = max(confidence, score_magic(len(magic)))
                breakdown["bom"] = float(len(magic))
                break

        # 3. DOCTYPE
        if self.DOCTYPE_RE.search(window):
            confidence = max(confidence, score_tokens(0.6))
            breakdown["doctype"] = 1.0

        # 4. Parse attempt
        if token_ratio > 0 and self._parse_snippet(window):
            confidence = max(confidence, score_tokens(1.0))
            breakdown["parsed"] = 1.0

        # 5. Root tag detection
        stripped = window.lstrip()
        if stripped.startswith("<") and ">" in stripped:
            tag = stripped[1 : stripped.find(">")].split()[0].strip("/?")
            if tag:
                confidence = max(confidence, score_tokens(0.7))
                breakdown["root_tag"] = 1.0

        # 6. Balanced tag heuristic
        open_tags = len(self.OPEN_TAG_RE.findall(window))
        close_tags = len(self.CLOSE_TAG_RE.findall(window))
        if open_tags and abs(open_tags - close_tags) <= 2:
            confidence = max(confidence, score_tokens(0.6))
            breakdown["balanced"] = 1.0

        # 7. Token ratio (already computed above)
        if token_ratio > self.TOKEN_RATIO_THRESHOLD:
            confidence = max(confidence, score_tokens(min(token_ratio, 0.9)))
        breakdown["token_ratio"] = round(token_ratio, 3)


        
        if confidence == 0 or b"%PDF-" in payload:
            return Result(candidates=[])
        
        if b'<!DOCTYPE html' in payload or b'<!DOCTYPE HTML' in payload or b'<html' in payload or b'<HTML' in payload:
            cand.append(
                    Candidate(
                        media_type="text/html",
                        extension="html",
                        confidence=1,
                        breakdown=breakdown,
                    )
                )
            return Result(candidates=cand)

        return self._make_result(confidence, breakdown)
