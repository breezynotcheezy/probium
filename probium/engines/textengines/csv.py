from ...models import Candidate
import re
import csv
import io
from functools import lru_cache
from typing import Optional


def ceck(text: str) -> Candidate | None:
    patterns = [r"@echo\s+off", r"\brem\b"]
    if any(re.search(p, text, re.IGNORECASE) for p in patterns):
        return Candidate(
            media_type="application/x-bat",
            extension="bat",
            confidence=1.0,
            breakdown={"lang": "batch"}
        )
    return None


def detect_delimiter(sample: str) -> Optional[str]:
    """Fallback method to detect the delimiter if csv.Sniffer fails."""

    DELIMS = ",;\t|"
    MIN_ROWS = 3
    SAMPLE_LINES = 20
    SAMPLE_SIZE = 4096  # bytes for initial analysis
    CHUNK_SIZE = 8192  # bytes for streaming
    _TOKEN_RE = re.compile(r"[,\t;|]")


    candidates = list(DELIMS)
    scores = {}
    for d in candidates:
        counts = [ln.count(d) for ln in sample.splitlines() if ln.strip()]
        if counts and len(set(counts)) == 1 and counts[0] > 0:
            scores[d] = counts[0]
    if scores:
        delim = max(scores, key=scores.get)
        #logger.debug("Detected delimiter: %s", delim)
        return delim
    #logger.debug("No consistent delimiter found")
    return None

@lru_cache(maxsize=128)
def _analyze_sample(text_sample: str) -> tuple:
    """Analyze a sample of text, cached by payload hash."""

    DELIMS = ",;\t|"
    MIN_ROWS = 3
    SAMPLE_LINES = 20
    SAMPLE_SIZE = 4096  # bytes for initial analysis
    CHUNK_SIZE = 8192  # bytes for streaming
    _TOKEN_RE = re.compile(r"[,\t;|]")

    lines = text_sample.splitlines()[:SAMPLE_LINES]
    sample = '\n'.join(lines)
    if not sample.strip():
        #logger.debug("Sample is empty after stripping")
        return None, None, [], 0.0, 0.0

    # Detect delimiter
    try:
        dialect = csv.Sniffer().sniff(sample, DELIMS)
        #logger.debug("csv.Sniffer detected delimiter: %s", dialect.delimiter)
    except Exception:
        delim = detect_delimiter(sample)
        if not delim:
            #logger.debug("Fallback delimiter detection failed")
            return None, None, [], 0.0, 0.0
        dialect = csv.excel()
        dialect.delimiter = delim

    # Parse rows
    try:
        reader = csv.reader(io.StringIO(sample), dialect)
        rows = [row for row in reader if row]
    except Exception as e:
        #logger.debug("CSV parsing failed: %s", e)
        return None, None, [], 0.0, 0.0

    if len(rows) < MIN_ROWS:
        #logger.debug("Too few rows: %d < %d", len(rows), self.MIN_ROWS)
        return None, None, [], 0.0, 0.0

    # Analyze column consistency
    column_counts = [len(r) for r in rows]
    if not column_counts:
        return None, None, [], 0.0, 0.0
    
    

    most_common_count = max(set(column_counts), key=column_counts.count)

    consistency_ratio = column_counts.count(most_common_count) / len(rows)
    token_count = sum(len(_TOKEN_RE.findall(ln)) for ln in lines)
    total_chars = sum(len(ln) for ln in lines)
    token_ratio = token_count / total_chars if total_chars > 0 else 0

    try:
        has_header = csv.Sniffer().has_header(sample)
    except Exception:
        #logger.debug("csv.Sniffer.has_header failed")
        has_header = False

    return dialect, has_header, rows, consistency_ratio, token_ratio

###
### change to candidate
### change sniff to something else
###
def check_csv(text: str) -> Candidate:
    """Detect if the payload is a CSV file with improved robustness and performance."""

    MAGIC_PATTERNS = ['sep=', '#', '"', ',']
    CONSISTENCY_THRESHOLD = 0.5
    TOKEN_RATIO_THRESHOLD = 0.01
    # Confidence levels
    MAGIC_CONFIDENCE = 0.9
    HIGH_CONFIDENCE = 0.8
    MEDIUM_CONFIDENCE = 0.5
    HEADER_BOOST = 0.1

    # Check magic patterns
    magic_len = None
    for m in MAGIC_PATTERNS:
        if text.startswith(m):
            magic_len = len(m)
            #logger.debug("Magic pattern matched: %s", m)
            break

    # Analyze sample with caching
    dialect, has_header, rows, consistency_ratio, token_ratio = _analyze_sample(text)
    if not rows:
        return None

    #print(rows)
    first_row_len = len(rows[0])
    if any(len(row) > first_row_len for row in rows[1:]):
        return None  # Reject: row longer than header

    if consistency_ratio < CONSISTENCY_THRESHOLD:
        #logger.debug("Consistency ratio too low: %.2f", consistency_ratio)
        return None
    
    #print(consistency_ratio)

    # Calculate confidence
    base_conf = MEDIUM_CONFIDENCE
    if consistency_ratio > 0.8:
        base_conf = HIGH_CONFIDENCE
    elif consistency_ratio > CONSISTENCY_THRESHOLD:
        base_conf += 0.1
    if has_header:
        base_conf += HEADER_BOOST
        #logger.debug("Header detected, boosting confidence")
    if magic_len:
        base_conf = max(base_conf, MAGIC_CONFIDENCE)
    if token_ratio > TOKEN_RATIO_THRESHOLD:
        base_conf += 0.1
        #logger.debug("Token ratio sufficient: %.3f", token_ratio)

    conf = min(base_conf, 1.0)
    #logger.debug("Final confidence: %.2f", conf)

    partial = False



    breakdown = {
            "token<|control630|>": round(token_ratio, 3),
            "partial": partial,
            "consistency_ratio": round(consistency_ratio, 3),
        }
    
    if magic_len is not None:
        breakdown["magic_len"] = magic_len

    return Candidate(
        media_type="text/csv",
        extension="csv",
        confidence=conf,
        breakdown=breakdown,
    )
    
