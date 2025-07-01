from __future__ import annotations
from ..models import Candidate, Result
from ..scoring import score_magic, score_tokens
from .base import EngineBase
from ..registry import register
import re


@register
class PDFEngine(EngineBase):
    name = "pdf"
    cost = 0.1
    _MAGIC = b"%PDF-" # in-house

    def sniff(self, payload: bytes) -> Result:
        window = payload[:1024]#check first 8 bytes
        idx = window.find(self._MAGIC)
        cand = []
   
        #if idx != -1:
        #conf = score_magic(len(self._MAGIC))
        conf = 1
        
        eof = b'%%EOF' in payload
        xref = b'xref' in payload
        trailer = b'trailer' in payload

        cat_pattern = rb'/Type\s*/Catalog'
        catalog = re.search(cat_pattern, payload) is not None

        page_pattern = rb'/Type\s*/Page'
        pages = re.search(page_pattern, payload) is not None
        
        obj_endobj_pattern = rb'\d+\s+\d+\s*obj.*?endobj'
        contains_obj_block = re.search(obj_endobj_pattern, payload, re.DOTALL | re.S) is not None

        final_xref_eof_pattern = rb'startxref\s*\d+\s*%%EOF'
        contains_final_xref_eof = re.search(final_xref_eof_pattern, payload, re.DOTALL | re.S) is not None

        stream_pattern = rb'stream.*?endstream'
        contains_stream = re.search(stream_pattern, payload, re.DOTALL | re.S) is not None

        ptex = b'/PTEX.PageNumber' in payload
       

        xref_startxref_pattern = rb'xref.*?startxref'
        contains_xtos = re.search(xref_startxref_pattern, payload, re.DOTALL | re.S) is not None


        sum = eof + xref + contains_final_xref_eof + contains_obj_block + ptex + contains_stream + pages + catalog

        #print(sum)
        if sum >= 5:
            conf = 1.0

            if idx == -1:
                conf -= 0.05
                cand.append(
                Candidate(
                    media_type="application/pdf",
                    extension="pdf",
                    confidence=conf,
                    breakdown={"offset": float(idx), "magic_len": float(len(self._MAGIC))},
                ))
                return Result(candidates=cand, error="PDF file is corrupted, no PDF version header found")
            else:
                cand.append(
                Candidate(
                    media_type="application/pdf",
                    extension="pdf",
                    confidence=conf,
                    #breakdown={"offset": float(idx), "magic_len": float(len(self._MAGIC))},
                ))
        
        return Result(candidates=cand)
