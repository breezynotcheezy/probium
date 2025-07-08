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

        #stream_pattern = rb'stream.*?endstream'
        stream_pattern = rb'>>\s*stream\s*x?[\x00-\xff]{2,}'
        contains_stream = re.search(stream_pattern, payload, re.DOTALL | re.S) is not None

        ptex = b'/PTEX.PageNumber' in payload
       

        xref_startxref_pattern = rb'xref.*?startxref'
        contains_xtos = re.search(xref_startxref_pattern, payload, re.DOTALL | re.S) is not None

        filter_pattern = rb'/Filter\s*/FlateDecode'
        filter = re.search(filter_pattern, payload) is not None

        width_pattern = rb'/Width\s+\d+'
        height_pattern = rb'/Height\s+\d+'


        image_blocks = list(re.finditer(rb'<<.*?/Subtype\s*/Image.*?>>', payload, re.DOTALL))
        valid_image_blocks = 0

        for match in image_blocks:
            block = match.group()
            if re.search(width_pattern, block) and re.search(height_pattern, block):
                valid_image_blocks += 1

        contains_image_with_dims = valid_image_blocks > 0

        #stream_obj_pattern = rb'/Type\s*/Stream\s*>>\s*stream\s*x[\x00-\xff]{2,}'
        #contains_stream_obj = re.search(stream_obj_pattern, payload) is not None

        bin_comment_pattern = rb'%[\x80-\xFF]{4,}.*?(?:\r?\n|$)'
        bin_comment = re.search(bin_comment_pattern, payload) is not None

        contains_sig = idx >= 0

        payload_size = len(payload)
        score = eof + xref + contains_final_xref_eof + contains_obj_block + ptex + contains_stream + pages + catalog + contains_xtos + filter + contains_image_with_dims + bin_comment + contains_sig

        # Dynamically determine score threshold
        if payload_size <= 8192:
            score_threshold = 2
        elif payload_size <= 16384:
            score_threshold = 4
        else:  
            score_threshold = 6

        if score >= score_threshold:
            conf = 1.0
                
            if idx == -1:
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
                    breakdown={"offset": float(idx), "magic_len": float(len(self._MAGIC)), "score": score},
                ))
        
        return Result(candidates=cand)
