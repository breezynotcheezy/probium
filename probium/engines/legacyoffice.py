from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
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


    def olefile_detect(self, payload: bytes, idx: int) -> Candidate | None:
        if olefile is None:
            return None

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

            conf = 1.0
            if idx != 0:
                conf *= 0.9

            return Candidate(
                media_type=mtype,
                extension=ext,
                confidence=conf,
                breakdown={"offset": float(idx)},
            )

        except Exception:
            return Candidate(
                media_type="application/vnd.ms-office",
                extension="cfb",
                confidence=0.5,
                breakdown={"offset": float(idx), "error": -1},
            )


    def sniff(self, payload: bytes) -> Result:
        window = payload[:1 << 20]  # scan first 1MB
        idx = window.find(self._MAGIC)
        cand = []
        if idx != -1:
            
            if len(payload) > 8192:
                ole_result = self.olefile_detect(payload, idx)
                if ole_result:
                    #print("result")
                    cand.append(ole_result)
                    return Result(candidates=cand)

            decoded = payload.decode("utf-8", errors="ignore")
            text = decoded.replace('\x00', '')

            if b'\x09\x08\x10\x00' in payload or 'Workbook' in text:
                cand.append(
                    Candidate(
                        media_type="application/vnd.ms-excel",
                        extension="xls",
                        confidence=1,
                        breakdown={"offset": float(idx)},
                    )
                )
                return Result(candidates=cand) 
            
            if b'\xEC\xA5\xC1\x00' in payload or b'\xDC\xA5\x68\x00' in payload or 'MSWord' in text or 'Microsoft Word' in text or 'WordDocument' in text:
                cand.append(
                    Candidate(
                        media_type="application/msword",
                        extension="doc",
                        confidence=1,
                        breakdown={"offset": float(idx)},
                    )
                )
                return Result(candidates=cand)
            
            if b'\xA0\x46\x1D\xF0' in payload or b'\x60\x21\x1B\xF0' in payload or b'\x00\x6E\x1E\xF0' in payload or b'\x00\x6E\x1E\xF0' in payload or b'\x0F\x00\xE8\x03' in payload or b'\x40\x3D\x1A\xF0' in payload or 'PowerPoint' in text:
                cand.append(
                    Candidate(
                        media_type="application/vnd.ms-powerpoint",
                        extension="ppt",
                        confidence=1,
                        breakdown={"offset": float(idx)},
                    )
                )
                return Result(candidates=cand)

            
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

                #print(ext)
                
                #conf = score_magic(len(self._MAGIC))
                conf = 1.0
                if idx != 0:
                    conf *= 0.9
                cand.append(
                    Candidate(
                        media_type=mtype,
                        extension=ext,
                        confidence=conf,
                        breakdown={"offset": float(idx)},
                    )
                )
            except Exception:
                #print("exception")
                #print(f"payload: \n{text}\n")
                cand.append(
                    Candidate(
                        media_type="application/vnd.ms-office",
                        extension="cfb",
                        confidence=0.5,
                        breakdown={"offset": float(idx), "error": -1},
                    )
                )
        return Result(candidates=cand)