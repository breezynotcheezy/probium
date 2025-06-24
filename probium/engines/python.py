from __future__ import annotations

from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
import logging
import mimetypes
import importlib.util
from ..libmagic import load_magic
from ..scoring import score_magic, score_tokens

logger = logging.getLogger(__name__)

_magic = load_magic()
_PYC_MAGIC = importlib.util.MAGIC_NUMBER

_PY_SHEBANG = b"python"

@register
class PythonEngine(EngineBase):
    name = "python"
    cost = 0.01

    def sniff(self, payload: bytes) -> Result:
        if payload.startswith(_PYC_MAGIC):
            conf = score_magic(len(_PYC_MAGIC))
            cand = Candidate(
                media_type="application/x-python-bytecode",
                extension="pyc",
                confidence=conf,
                breakdown={"magic_len": float(len(_PYC_MAGIC))},
            )
            return Result(candidates=[cand])

        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover - libmagic errors
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "python" in mime:
                    conf = score_magic(len(_PYC_MAGIC))
                    cand = Candidate(
                        media_type="text/x-python",
                        extension="py",
                        confidence=conf,
                        breakdown={"magic_len": float(len(_PYC_MAGIC))},
                    )
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first_line = text.splitlines()[0] if text else ""
        if first_line.startswith("#!") and "python" in first_line:
            cand = Candidate(
                media_type="text/x-python",
                extension="py",
                confidence=score_tokens(1.0),
                breakdown={"token_ratio": 1.0},
            )
            return Result(candidates=[cand])
        head = text[:512]
        tokens = ["def ", "import ", "class ", "__name__", "from ", "async def "]
        if any(tok in head for tok in tokens):
            hits = sum(tok in head for tok in tokens)
            ratio = hits / len(tokens)
            cand = Candidate(
                media_type="text/x-python",
                extension="py",
                confidence=score_tokens(ratio),
                breakdown={"token_ratio": ratio},
            )
            return Result(candidates=[cand])
        return Result(candidates=[])
