#made for zip files - recursive scan example engine
from __future__ import annotations
from ..scoring import score_magic, score_tokens
import zipfile, io, re, xml.etree.ElementTree as ET
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
            cand.append(
                Candidate(media_type="application/zip", extension="zip", confidence=0.98)
            )
            return Result(candidates=cand, error="Couldn't read entire zip file")
        return Result(candidates=cand)
