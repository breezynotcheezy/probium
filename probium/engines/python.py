from __future__ import annotations

from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register

_PY_SHEBANG = b"python"

@register
class PythonEngine(EngineBase):
    name = "python"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return Result(candidates=[])
        first_line = text.splitlines()[0] if text else ""
        if first_line.startswith("#!") and "python" in first_line:
            return Result(candidates=[Candidate(media_type="text/x-python", extension="py", confidence=0.99)])
        head = text[:256]
        if any(tok in head for tok in ("def ", "import ", "class ", "__name__")):
            return Result(candidates=[Candidate(media_type="text/x-python", extension="py", confidence=0.8)])
        return Result(candidates=[])
