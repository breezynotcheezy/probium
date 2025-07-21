#made for zip files - recursive scan example engine
from __future__ import annotations
from ..scoring import score_magic, score_tokens
import zipfile, io, re, xml.etree.ElementTree as ET, struct, zlib
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_SIGS = {
    "[Content_Types].xml": {
        "word/": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx"),
        "ppt/": ("application/vnd.openxmlformats-officedocument.presentationml.presentation", "pptx"),
        "xl/": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"),
    },
    "mimetype": {
        "application/vnd.oasis.opendocument.text": ("application/vnd.oasis.opendocument.text", "odt"),
        "application/vnd.oasis.opendocument.presentation": ("application/vnd.oasis.opendocument.presentation", "odp"),
        "application/vnd.oasis.opendocument.spreadsheet": ("application/vnd.oasis.opendocument.spreadsheet", "ods"),
    },
}
@register
class ZipOfficeEngine(EngineBase):
    name = "zipoffice"
    cost = 0.5

    SAMPLE_SIZE = 4096
    TOKEN_RE = re.compile(r"[<>]")

    def sniff(self, payload: bytes) -> Result:
        if not payload.startswith(b"PK\x03\x04"):
            return Result(candidates=[])
        cand = []

        ctypes = b"[Content_Types].xml" in payload

        # docx files
        num = b"\x00\x00word/numbering.xml" in payload
        set = b"\x00\x00word/settings.xml" in payload
        font = b"\x00\x00word/fontTable.xml" in payload
        styles = b"\x00\x00styles.xml" in payload
        doc = b"\x00\x00word/document.xml" in payload

        """ if ctypes: print("ctypes")
        if num: print("num")
        if set: print("set")
        if font: print("font")
        if styles: print("styles")
        if doc: print("doc") """
       
        docxsum = ctypes + num + set + font + styles + doc

        if docxsum >= 2:
            cand.append(
                        Candidate(
                            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            extension="docx",
                            confidence=1.0,
                            breakdown={"token_ratio": 1.0},
                        )
                    )
            return Result(candidates=cand)

        # pptx files
        rel = b"ppt/_rels" in payload
        draw = b"ppt/drawings" in payload
        embed = b"ppt/embeddings" in payload
        media = b"ppt/media" in payload
        notem = b"ppt/notesMasters" in payload
        notes = b"ppt/notesSlides" in payload
        slidel = b"ppt/slideLayouts" in payload
        slidem = b"ppt/slideMasters" in payload
        slides = b"ppt/slides" in payload
        theme = b"ppt/theme" in payload
        pres = b"ppt/presentation.xml" in payload
        presp = b"ppt/presProps.xml" in payload
        table = b"ppt/tableStyles.xml" in payload
        view = b"ppt/viewProps.xml" in payload

        """ if rel: print("Found: ppt/_rels")
        if draw: print("Found: ppt/drawings")
        if embed: print("Found: ppt/embeddings")
        if media: print("Found: ppt/media")
        if notem: print("Found: ppt/notesMasters")
        if notes: print("Found: ppt/notesSlides")
        if slidel: print("Found: ppt/slideLayouts")
        if slidem: print("Found: ppt/slideMasters")
        if slides: print("Found: ppt/slides")
        if theme: print("Found: ppt/theme")
        if pres: print("Found: ppt/presentation.xml")
        if presp: print("Found: ppt/presProps.xml")
        if table: print("Found: ppt/tableStyles.xml")
        if view: print("Found: ppt/viewProps.xml") """

        pptxsum = rel + draw + embed + media + notem + notes + slidel + slidem + slides + theme + pres + presp + table + view + ctypes
        
        if pptxsum >= 2:
            cand.append(
                        Candidate(
                            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            extension="pptx",
                            confidence=1.0,
                            breakdown={"token_ratio": 1.0},
                        )
                    )
            return Result(candidates=cand)

        # xlsx files
        rel = b"xl/_rels" in payload
        workb = b"xl/workbook.xml" in payload
        works = b"xl/worksheets/" in payload
        calc = b"xl/calcChain.xml" in payload
        styles = b"xl/styles.xml" in payload
        shared = b"xl/sharedStrings.xml" in payload
        printer = b"xl/printerSettings/" in payload
        theme = b"xl/theme/" in payload
        draw = b"xl/drawings/" in payload
        media = b"xl/media/" in payload

        xlsxsum = rel + workb + works + calc + styles + shared + printer + theme + draw + media + ctypes

        if xlsxsum >= 3:
            cand.append(
                        Candidate(
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            extension="xlsx",
                            confidence=1.0,
                            breakdown={"token_ratio": 1.0},
                        )
                    )
            return Result(candidates=cand)
        
        if b"META-INF/MANIFEST.MF" in payload:
            cand.append(
                        Candidate(
                            media_type="application/java-archive",
                            extension="jar",
                            confidence=1.0,
                            breakdown={"token_ratio": 1.0},
                        )
                    )
            return Result(candidates=cand)

        try:
            with zipfile.ZipFile(io.BytesIO(payload)) as zf:
                namelist = zf.namelist()
                found_type = False

                if "[Content_Types].xml" in namelist:
                    for dir_, (mime, ext) in _SIGS["[Content_Types].xml"].items():
                        if any(n.startswith(dir_) for n in namelist):
                            cand.append(
                                Candidate(
                                    media_type=mime,
                                    extension=ext,
                                    confidence=score_tokens(1.0),
                                    breakdown={"token_ratio": 1.0},
                                )
                            )
                            found_type = True
                            break

                if "mimetype" in namelist and not found_type:
                    mime = zf.read("mimetype").decode(errors="ignore").strip()
                    if mime in _SIGS["mimetype"]:
                        mt, ext = _SIGS["mimetype"][mime]
                        breakdown = {"mimetype": 1.0}

                        required = {"content.xml", "meta.xml"}
                        hits = sum(1 for r in required if r in namelist)
                        breakdown["required_ratio"] = hits / len(required)

                        token_ratio = 0.0
                        parsed = False
                        if "content.xml" in namelist:
                            text = (
                                zf.read("content.xml")[: self.SAMPLE_SIZE]
                                .decode("utf-8", errors="ignore")
                            )
                            token_ratio = len(self.TOKEN_RE.findall(text)) / max(len(text), 1)
                            breakdown["token_ratio"] = round(token_ratio, 3)
                            if "<office:" in text:
                                breakdown["root_tag"] = 1.0
                            try:
                                ET.fromstring(text)
                                parsed = True
                            except Exception:
                                parsed = False
                        if parsed:
                            breakdown["parsed"] = 1.0

                        conf = score_magic(len(mime))
                        if hits == len(required) and parsed:
                            conf = 1.0
                        cand.append(
                            Candidate(
                                media_type=mt,
                                extension=ext,
                                confidence=conf,
                                breakdown=breakdown,
                            )
                        )
                        found_type = True

                if not found_type:
                    cand.append(
                        Candidate(
                            media_type="application/zip",
                            extension="zip",
                            confidence=score_tokens(0.05),
                            breakdown={"token_ratio": 0.05},
                        )
                    )
        except Exception:
            # Fallback for truncated archives: try to parse first entry directly
            try:
                sig, ver, flags, method, mtime, mdate, crc, csize, usize, nlen, elen = struct.unpack_from(
                    "<IHHHHHIIIHH", payload, 0
                )
                name = payload[30 : 30 + nlen].decode("utf-8", errors="ignore")
                data_start = 30 + nlen + elen
                data = payload[data_start : data_start + csize]
                if len(data) == csize and name == "mimetype":
                    content = data if method == 0 else zlib.decompress(data)
                    mime = content.decode(errors="ignore").strip()
                    if mime in _SIGS["mimetype"]:
                        mt, ext = _SIGS["mimetype"][mime]
                        cand.append(
                            Candidate(
                                media_type=mt,
                                extension=ext,
                                confidence=score_magic(len(mime)),
                                breakdown={"partial": 1.0},
                            )
                        )
                        return Result(candidates=cand)
            except Exception:
                pass
            cand.append(
                Candidate(media_type="application/zip", extension="zip", confidence=0.98)
            )
            return Result(candidates=cand, error="Couldn't read entire zip file")
        return Result(candidates=cand)
