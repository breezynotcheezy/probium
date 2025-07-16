from ...models import Candidate
import re
from ...scoring import score_tokens, score_magic
from functools import lru_cache
import xml.etree.ElementTree as ET


@lru_cache(maxsize=64)
def _parse_snippet(snippet: str) -> bool:
    """Attempt to parse a snippet of XML, cached by content."""
    try:
        ET.fromstring(snippet)
        return True
    except Exception:
        try:
            ET.fromstring(f"<root>{snippet}</root>")
            return True
        except Exception:
            return False
            
def check_xml(text: str, payload: bytes) -> Candidate | None:
    SAMPLE_SIZE = 4096
    TOKEN_RATIO_THRESHOLD = 0.05

    BOM_UTF8 = b"\xEF\xBB\xBF"
    BOM_UTF16_LE = b"\xFF\xFE"
    BOM_UTF16_BE = b"\xFE\xFF"
    MAGIC_PATTERNS = [BOM_UTF8, BOM_UTF16_LE, BOM_UTF16_BE, b"<?xml"]

    DECL_RE = re.compile(r"<\?xml[^>]*>")
    DOCTYPE_RE = re.compile(r"<!DOCTYPE[^>]+>", re.I)
    TOKEN_RE = re.compile(r"[<>]")
    OPEN_TAG_RE = re.compile(r"<[^/!?][^>]*>")
    CLOSE_TAG_RE = re.compile(r"</[^>]+>")

    cand=[]

    window = text[:SAMPLE_SIZE]
    breakdown: dict[str, float] = {}
    conf = 0.0

    token_ratio = len(TOKEN_RE.findall(window)) / max(len(window), 1)

    if token_ratio < TOKEN_RATIO_THRESHOLD / 4:
        return None

    # 2. XML declaration / BOM
    if window.lstrip().startswith("<?xml"):
        conf = max(conf, score_magic(5))
        breakdown["xml_decl"] = 1.0
    for magic in (BOM_UTF8, BOM_UTF16_LE, BOM_UTF16_BE):
        if payload.startswith(magic):
            conf = max(conf, score_magic(len(magic)))
            breakdown["bom"] = float(len(magic))
            break

    # 3. DOCTYPE
    if DOCTYPE_RE.search(window):
        conf = max(conf, score_tokens(0.6))
        breakdown["doctype"] = 1.0

    # 4. Parse attempt
    if token_ratio > 0 and _parse_snippet(window):
        conf = max(conf, score_tokens(1.0))
        breakdown["parsed"] = 1.0

    # 5. Root tag detection
    stripped = window.lstrip()
    if stripped.startswith("<") and ">" in stripped:
        tag = stripped[1 : stripped.find(">")].split()[0].strip("/?")
        if tag:
            conf = max(conf, score_tokens(0.7))
            breakdown["root_tag"] = 1.0

    # 6. Balanced tag heuristic
    open_tags = len(OPEN_TAG_RE.findall(window))
    close_tags = len(CLOSE_TAG_RE.findall(window))
    if open_tags and abs(open_tags - close_tags) <= 2:
        conf = max(conf, score_tokens(0.6))
        breakdown["balanced"] = 1.0

    # 7. Token ratio (already computed above)
    if token_ratio > TOKEN_RATIO_THRESHOLD:
        conf = max(conf, score_tokens(min(token_ratio, 0.9)))
    breakdown["token_ratio"] = round(token_ratio, 3)


    
    if conf == 0 or b"%PDF-" in payload:
        return None
    
    if b'<!DOCTYPE html' in payload or b'<!DOCTYPE HTML' in payload or b'<html' in payload or b'<HTML' in payload or b'<a href=' in payload:
        cand = Candidate(
                    media_type="text/html",
                    extension="html",
                    confidence=1.0,
                    breakdown=breakdown,
                )
        return cand

    cand = Candidate(
            media_type="application/xml",
            extension="xml",
            confidence=conf,
            breakdown=breakdown,
        )
    return cand
    #return self._make_result(confidence, breakdown)