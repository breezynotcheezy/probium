from __future__ import annotations
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
import logging
import mimetypes
import magic

logger = logging.getLogger(__name__)

try:
    _magic = magic.Magic(mime=True)
except Exception as exc:  # pragma: no cover
    logger.warning("libmagic unavailable: %s", exc)
    _magic = None

@register
class XMLEngine(EngineBase):
    name = "xml"
    cost = 0.05
    _MAGIC = [b'\xEF\xBB\xBF', b'\xFF\xFE', b'\xFE\xFF', b"<?xml"]

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "xml" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "xml"
                    cand = Candidate(media_type=mime, extension=ext, confidence=0.95)
                    return Result(candidates=[cand])

        window = payload[:64]
        cand = []

        for magic in self._MAGIC:
            idx = window.find(magic)
            if idx != -1:
                conf = 1.0 if idx == 0 else 0.90 - min(idx / (1 << 20), 0.1)
                cand.append(
                    Candidate(
                        media_type="application/xml",
                        extension="xml",
                        confidence=conf,
                    )
                )
                break

        if not cand and window.lstrip().startswith(b"<") and b">" in window:
            cand.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=0.6,
                )
            )

        return Result(candidates=cand)
