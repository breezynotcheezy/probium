from __future__ import annotations
import re
import mimetypes
import logging
import xml.etree.ElementTree as ET

from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()

@register
class XMLEngine(EngineBase):
    name = "xml"
    cost = 0.05
    _MAGIC = [b"\xEF\xBB\xBF", b"\xFF\xFE", b"\xFE\xFF", b"<?xml"]
    _TOKEN_RE = re.compile(r"[<>]")

    def _make_result(self, conf: float, breakdown: dict[str, float]) -> Result:
        cand = Candidate(
            media_type="application/xml",
            extension="xml",
            confidence=conf,
            breakdown=breakdown,
        )
        return Result(candidates=[cand])

    def sniff(self, payload: bytes) -> Result:
        # Layer 1: libmagic
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "xml" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "xml"
                    cand = Candidate(
                        media_type=mime,
                        extension=ext,
                        confidence=score_tokens(1.0),
                        breakdown={"libmagic": True},
                    )
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])

        window = text[:256]
        candidates: list[Candidate] = []

        # Layer 2: BOM detection
        for magic in self._MAGIC[:3]:
            if payload.startswith(magic):
                candidates.append(
                    Candidate(
                        media_type="application/xml",
                        extension="xml",
                        confidence=score_magic(len(magic)),
                        breakdown={"bom": float(len(magic))},
                    )
                )
                break

        # Layer 3: XML declaration
        if window.lstrip().startswith("<?xml"):
            candidates.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=score_magic(5),
                    breakdown={"xml_decl": 1.0},
                )
            )

        # Layer 4: attempt parsing
        try:
            ET.fromstring(text)
            candidates.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=score_tokens(1.0),
                    breakdown={"parsed": 1.0},
                )
            )
        except Exception:
            pass

        # Layer 5: root tag detection
        stripped = window.lstrip()
        if stripped.startswith("<") and ">" in stripped:
            tag = stripped[1:stripped.find(">")].split()[0].strip("/?")
            if tag:
                candidates.append(
                    Candidate(
                        media_type="application/xml",
                        extension="xml",
                        confidence=score_tokens(0.2),
                        breakdown={"root_tag": 1.0},
                    )
                )

        # Layer 6: balanced tags heuristic
        open_tags = len(re.findall(r"<[^/!?][^>]*>", window))
        close_tags = len(re.findall(r"</[^>]+>", window))
        if open_tags and abs(open_tags - close_tags) <= 2:
            candidates.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=score_tokens(0.15),
                    breakdown={"balanced": 1.0},
                )
            )

        # Layer 7: token ratio
        token_ratio = len(self._TOKEN_RE.findall(window)) / max(len(window), 1)
        if token_ratio > 0.05:
            candidates.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=score_tokens(min(token_ratio, 0.7)),
                    breakdown={"token_ratio": round(token_ratio, 3)},
                )
            )

        if not candidates:
            return Result(candidates=[])

        best = max(candidates, key=lambda c: c.confidence)
        return Result(candidates=[best])
