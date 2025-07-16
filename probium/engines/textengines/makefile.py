from ...models import Candidate
import re

def check(text: str) -> Candidate | None:

    patterns = [
        r"^\s*CC\s*[:?]?=",           # matches CC = or CC := or CC?=
        r"^\s*CFLAGS\s*[:?]?=",       # matches CFLAGS = or CFLAGS :=
        r"-Wall\b",                   # matches -Wall as a separate flag
        r"-Werror\b",                 # matches -Werror
    ]
    matches = sum(1 for p in patterns if re.search(p, text, re.MULTILINE))
    #if any(re.search(p, text, re.MULTILINE) for p in patterns):
    if matches >= 2:
        return Candidate(
            media_type="text/x-makefile",
            extension="mk",
            confidence=1.0,
            breakdown={"lang": "C makefile", "matched": "makefile pattern"}
        )
    return None