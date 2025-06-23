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
class PowerShellEngine(EngineBase):
    name = "powershell"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "powershell" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "ps1"
                    cand = Candidate(media_type=mime, extension=ext, confidence=0.95)
                    return Result(candidates=[cand])

        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        if text.lstrip().startswith("#requires") or "Write-Host" in text:
            return Result(candidates=[Candidate(media_type="text/x-powershell", extension="ps1", confidence=0.9)])
        return Result(candidates=[])
