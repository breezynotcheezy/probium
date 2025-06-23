from __future__ import annotations
import logging
import mimetypes
import magic
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

logger = logging.getLogger(__name__)

@register
class MagicLibEngine(EngineBase):
    """Detect file types using libmagic."""

    name = "libmagic"
    cost = 0.02

    def __init__(self) -> None:
        super().__init__()
        try:
            self._magic = magic.Magic(mime=True)
        except Exception as exc:  # pragma: no cover - library issues
            logger.warning("libmagic unavailable: %s", exc)
            self._magic = None

    def sniff(self, payload: bytes) -> Result:
        if self._magic is None:
            return Result(candidates=[])
        try:
            mime = self._magic.from_buffer(payload)
        except Exception as exc:  # pragma: no cover - rare
            logger.warning("libmagic failed: %s", exc)
            return Result(candidates=[])
        if not mime:
            return Result(candidates=[])
        ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or None
        cand = Candidate(media_type=mime, extension=ext, confidence=0.9)
        return Result(candidates=[cand])
