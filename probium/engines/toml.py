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
class TomlEngine(EngineBase):
    name = "toml"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "toml" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "toml"
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
        if "=" in text and "[" in text and "]" in text and "\n" in text:
            if "[" in text.splitlines()[0]:
                cand = Candidate(
                    media_type="application/toml",
                    extension="toml",
                    confidence=score_tokens(1.0),
                    breakdown={"token_ratio": 1.0},
                )
                return Result(candidates=[cand])
        return Result(candidates=[])
