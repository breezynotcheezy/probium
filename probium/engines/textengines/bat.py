from ...models import Candidate
import re

def check(text: str) -> Candidate | None:
        patterns = [r"@echo\s+off", r"\brem\b"]
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            return Candidate(
                media_type="application/x-bat",
                extension="bat",
                confidence=1.0,
                breakdown={"lang": "batch"}
            )
        return None