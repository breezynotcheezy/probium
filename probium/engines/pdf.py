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
        """
        if idx != 0:
            conf *= 0.9
        """
        eof = b'%%EOF' in payload
        #print(f"eof: {eof}")

        xref = b'xref' in payload
        #print(f"xref: {xref}")

        trailer = b'trailer' in payload
        #print(f"trailer: {trailer}")


        cat_pattern = rb'/Type\s*/Catalog'
        catalog = re.search(cat_pattern, payload) is not None
        #print(f"catalog: {catalog}")

        page_pattern = rb'/Type\s*/Page'
        pages = re.search(page_pattern, payload) is not None
        #pages = b'/Type /Pages' in payload
        #print(f"pages: {pages}")


        obj_endobj_pattern = rb'\d+\s+\d+\s*obj.*?endobj'
        contains_obj_block = re.search(obj_endobj_pattern, payload, re.DOTALL | re.S) is not None
        #print(f"contains_obj_block: {contains_obj_block}")


        final_xref_eof_pattern = rb'startxref\s*\d+\s*%%EOF'
        contains_final_xref_eof = re.search(final_xref_eof_pattern, payload, re.DOTALL | re.S) is not None
        #print(f"contains_final_xref_eof: {contains_final_xref_eof}")

        stream_pattern = rb'stream.*?endstream'
        contains_stream = re.search(stream_pattern, payload, re.DOTALL | re.S) is not None
        #print(f"stream: {contains_stream}")

        ptex = b'/PTEX.PageNumber' in payload
        #print(f"ptex: {ptex}")

        

        """ 
        conf -= 0.2 if not eof else 0
        conf -= 0.2 if not xref else 0
        conf -= 0.2 if not trailer else 0
        conf = max(conf, 0.5)
        """

        sum = eof + xref + contains_final_xref_eof + contains_obj_block + ptex + contains_stream + pages + catalog

        if sum >= 5:
            conf = 1.0

            if idx == -1:
                conf -= 0.1
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
                    breakdown={"offset": float(idx), "magic_len": float(len(self._MAGIC))},
                ))
        
        return Result(candidates=cand)
