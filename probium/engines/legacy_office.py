from __future__ import annotations
from ..types import Candidate, Result
from .base import EngineBase
from ..registry import register
import io

try:  # optional dependency
    import olefile
except Exception:  # pragma: no cover - missing dependency
    olefile = None

@register
class LegacyOfficeEngine(EngineBase):
    name = "legacyoffice"
    cost = 0.1
    _MAGIC = b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"
    def sniff(self, payload: bytes) -> Result:
        window = payload[:1 << 20]  # scan first 1MB
        idx = window.find(self._MAGIC)
        cand = []
        if idx != -1:
            if olefile is None:
                return Result(candidates=[])
            try:
                ole = olefile.OleFileIO(io.BytesIO(payload))
                streams = ole.listdir(streams=True)
                flat_streams = ["/".join(path) for path in streams]

                if any(s.lower() == "worddocument" for s in flat_streams):
                    ext, mtype = "doc", "application/msword"
                elif any(s.lower() in ("workbook", "book") for s in flat_streams):
                    ext, mtype = "xls", "application/vnd.ms-excel"
                elif any(s.lower() == "powerpoint document" for s in flat_streams):
                    ext, mtype = "ppt", "application/vnd.ms-powerpoint"
                else:
                    ext, mtype = "cfb", "application/vnd.ms-office"

                conf = 1.0 if idx == 0 else 0.90 - min(idx / (1 << 20), 0.1)
                cand.append(
                    Candidate(
                        media_type=mtype,
                        extension=ext,
                        confidence=conf,
                        breakdown={"offset": float(idx)},
                    )
                )
            except Exception:
                cand.append(
                    Candidate(
                        media_type="application/vnd.ms-office",
                        extension="cfb",
                        confidence=0.5,
                        breakdown={"offset": float(idx), "error": -1},
                    )
                )
        return Result(candidates=cand)
