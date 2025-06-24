from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register

@register
class PDFEngine(EngineBase):
    name = "pdf"
    cost = 0.1
    _MAGIC = b"%PDF" # in-house

    def sniff(self, payload: bytes) -> Result:
        window = payload[:8]#check first 8 bytes
        idx = window.find(self._MAGIC)
        cand = []
        if idx != -1:
            conf = score_magic(len(self._MAGIC))
            if idx != 0:
                conf *= 0.9

            eof = b'%%EOF' in payload[-1024:]
            xref = b'xref' in payload[-4096:]
            trailer = b'trailer' in payload

            conf -= 0.2 if not eof else 0
            conf -= 0.2 if not xref else 0
            conf -= 0.2 if not trailer else 0
            conf = max(conf, 0.5)

            #print(f"conf: {conf}")
            cand.append(
                Candidate(
                    media_type="application/pdf",
                    extension="pdf",
                    confidence=conf,
                    breakdown={"offset": float(idx), "magic_len": float(len(self._MAGIC))},
                )
            )
        return Result(candidates=cand)
