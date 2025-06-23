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
class ZigEngine(EngineBase):
    name = "zig"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "zig" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "zig"
                    cand = Candidate(media_type=mime, extension=ext, confidence=0.95)
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "pub fn main" in text and "std.debug" in text:
            return Result(candidates=[Candidate(media_type="text/x-zig", extension="zig", confidence=0.9)])
        return Result(candidates=[])
