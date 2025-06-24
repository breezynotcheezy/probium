from __future__ import annotations
import os
from ..scoring import score_magic, score_tokens
import subprocess
import tempfile
import mimetypes
import shutil
import re
import logging
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register


logger = logging.getLogger(__name__)

_TRID_CMD = shutil.which("trid")

_missing_warning_logged = False

@register
class TridEngine(EngineBase):
    """Wrap the external `trid` tool if available."""
    name = "trid"
    cost = 5.0

    def sniff(self, payload: bytes) -> Result:
        global _missing_warning_logged
        if _TRID_CMD is None:
            if not _missing_warning_logged:
                logger.debug("trid command not found")
                _missing_warning_logged = True
            return Result(candidates=[])
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(payload)
            tmp.flush()
            path = tmp.name
        try:
            proc = subprocess.run([_TRID_CMD, "-n", path], capture_output=True, text=True)
        except Exception as exc:
            logger.exception("trid execution failed")
            os.unlink(path)
            return Result(candidates=[], error=str(exc))
        finally:
            if os.path.exists(path):
                os.unlink(path)

        if proc.returncode != 0:
            logger.warning("trid returned non-zero exit status %s", proc.returncode)
            return Result(candidates=[])

        candidates = []
        pattern = re.compile(r"([0-9.]+)% \(([^)]+)\) (.+)")
        for line in proc.stdout.splitlines():
            m = pattern.search(line)
            if not m:
                continue
            conf = float(m.group(1)) / 100.0
            ext = m.group(2).strip().lstrip('.')
            desc = m.group(3).strip()
            mime = mimetypes.guess_type(f"dummy.{ext}")[0] or "application/octet-stream"
            candidates.append(Candidate(media_type=mime, extension=ext, confidence=conf, breakdown={"trid": desc}))
        return Result(candidates=candidates)
