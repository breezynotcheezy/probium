from ...models import Candidate
import re

def check(text: str) -> Candidate | None:
    rust_use_pattern = re.compile(
        r"\buse\s+[a-zA-Z0-9_:{} ,]+;",
        re.MULTILINE
    )

    if rust_use_pattern.search(text):
        return Candidate(
            media_type="text/rust",
            extension="rs",
            confidence=1.0,
            breakdown={"lang": "rust", "pattern": "use statement"}
        )
    return None