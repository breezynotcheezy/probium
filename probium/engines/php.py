from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
import logging
import mimetypes
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()

@register
class PHPEngine(EngineBase):
    name = "php"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "php" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "php"
                    cand = Candidate(media_type=mime, extension=ext, confidence=0.95)
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.lstrip().startswith("<?php"):
            return Result(candidates=[Candidate(media_type="text/x-php", extension="php", confidence=0.95)])
        if "$" in text and "function" in text and "<?" in text:
            return Result(candidates=[Candidate(media_type="text/x-php", extension="php", confidence=0.8)])
        return Result(candidates=[])
