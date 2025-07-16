from ...models import Candidate
import re
import json
from ...scoring import score_tokens, score_magic


def _find_json_fragment(text: str) -> str | None:
    """Return the first valid JSON snippet inside ``text`` if present."""
    SAMPLE_SIZE = 65536

    decoder = json.JSONDecoder()
    snippet = text[:SAMPLE_SIZE]
    for match in re.finditer(r"[\{\[]", snippet):
        start = match.start()
        try:
            obj, idx = decoder.raw_decode(snippet[start:])
            end = start + idx
            return snippet[start:end]
        except Exception:
            continue
    return None


def check_json(text: str) -> Candidate | None:

    """Detect JSON using libmagic, magic bytes and structural analysis."""
    _TOKEN_RE = re.compile(r'[{}\[\]":,]')
    #these are not magic number sigs, "_MAGIC" field is used as placeholding binary sig. (delimiter replacement)
    _MAGIC = [b'{', b'[']

    # limit bytes inspected for expensive regex operations
    SAMPLE_SIZE = 65536

    
    stripped = text.lstrip()
    magic_hit = None
    for m in _MAGIC:
        if stripped.startswith(m.decode("latin1")):
            magic_hit = m
            break


    text = text.strip()
    if not text:
        return None

    #sample = text[:SAMPLE_SIZE]
    sample = text
    try:
        json.loads(text)
        parse_ok = True
    except Exception:
        parse_ok = False

    token_count = len(_TOKEN_RE.findall(sample))
    token_ratio = token_count / max(len(sample), 1)

    if parse_ok:
        conf = score_tokens(1.0)
        if magic_hit:
            conf = max(conf, score_magic(len(magic_hit)))
        #return self._make_result(conf, token_ratio, magic_len=len(magic_hit) if magic_hit else None)
        return Candidate(
                media_type="application/json",
                extension="json",
                confidence=1.0,
                breakdown={"lang": "json"}
            )
    # full parse failed, attempt partial analysis

    string_re = re.compile(r'"(?:\\.|[^"\\])*"')
    new_text = string_re.sub('', text)

    colon_count = new_text.count(":")
    brace_count = new_text.count("{") + new_text.count("}") + new_text.count("[") + new_text.count("]")
    
    ratio = 100
    if colon_count != 0 and brace_count != 0:
        ratio = brace_count / colon_count
        #print(ratio)

    #print(f"c: {colon_count}, b: {brace_count}, r: {ratio}\n\ntext: \n{text}\n")
    if ratio < 0.25 and '"' in sample:
        flat_key_val_pairs = re.findall(r'"\s*[^"]+\s*"\s*:\s*', text)
        if len(flat_key_val_pairs) > 5:
            return Candidate(
                media_type="application/json",
                extension="json",
                confidence=1.0,
                breakdown={"lang": "json"}
            )


    frag = _find_json_fragment(sample)
    if frag is not None:
        try:
            json.loads(frag)
            conf = score_tokens(min(0.9, token_ratio))
            if magic_hit:
                conf = max(conf, score_magic(len(magic_hit)))
            return Candidate(
                media_type="application/json",
                extension="json",
                confidence=1.0,
                breakdown={"lang": "json"}
            )

        except Exception:
            pass

    if token_ratio > 0.3 and ":" in text:
        conf = score_tokens(min(token_ratio, 0.8))
        

        if magic_hit:
            conf = max(conf, score_magic(len(magic_hit)))
        return Candidate(
                media_type="application/json",
                extension="json",
                confidence=1.0,
                breakdown={"lang": "json"}
            )


    return None
