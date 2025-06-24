from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
import logging
import mimetypes
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()

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
                    cand = Candidate(
                        media_type=mime,
                        extension=ext,
                        confidence=score_tokens(1.0),
                        breakdown={"token_ratio": 1.0},
                    )
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if "pub fn main" in text and "std.debug" in text:
            cand = Candidate(
                media_type="text/x-zig",
                extension="zig",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
