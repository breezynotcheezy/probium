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
except Exception as exc:  # pragma: no cover - lib setup
    logger.warning("libmagic unavailable: %s", exc)
    _magic = None

_PY_SHEBANG = b"python"

@register
class PythonEngine(EngineBase):
    name = "python"
    cost = 0.01

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover - libmagic errors
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "python" in mime:
                    cand = Candidate(media_type="text/x-python", extension="py", confidence=0.99)
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first_line = text.splitlines()[0] if text else ""
        if first_line.startswith("#!") and "python" in first_line:
            return Result(candidates=[Candidate(media_type="text/x-python", extension="py", confidence=0.99)])
        head = text[:512]
        tokens = ["def ", "import ", "class ", "__name__", "from ", "async def "]
        if any(tok in head for tok in tokens):
            return Result(candidates=[Candidate(media_type="text/x-python", extension="py", confidence=0.8)])
        return Result(candidates=[])
