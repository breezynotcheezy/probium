from ...models import Candidate
import re

def check(text: str) -> Candidate | None:
    patterns = [
        re.compile(r"\bdef\s+\w+\s*\((.*?)\):"),
        re.compile(r"\bimport\s+\w+"),
        re.compile(r"\bprint\s*\("),
        re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]"),
        re.compile(r"\bfrom\s+\w+\s+import\s+"),
    ]
    
    if any(p.search(text) for p in patterns):
        return Candidate(
            media_type="text/x-python",
            extension="py",
            confidence=1.0,
            breakdown={"lang": "python"}
        )
    return None