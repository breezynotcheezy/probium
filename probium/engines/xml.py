from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register
import logging
import mimetypes
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()

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
                    cand = Candidate(
                        media_type=mime,
                        extension=ext,
                        confidence=score_tokens(1.0),
                        breakdown={"token_ratio": 1.0},
                    )
                    return Result(candidates=[cand])

        window = payload[:64]
        cand = []

        for magic in self._MAGIC:
            idx = window.find(magic)
            if idx != -1:
                conf = score_magic(len(magic))
                if idx != 0:
                    conf *= 0.9
                cand.append(
                    Candidate(
                        media_type="application/xml",
                        extension="xml",
                        confidence=conf,
                        breakdown={"magic_len": float(len(magic)), "offset": float(idx)},
                    )
                )
                break

        if not cand and window.lstrip().startswith(b"<") and b">" in window:
            cand.append(
                Candidate(
                    media_type="application/xml",
                    extension="xml",
                    confidence=score_tokens(0.05),
                    breakdown={"token_ratio": 0.05},
                )
            )

        return Result(candidates=cand)
