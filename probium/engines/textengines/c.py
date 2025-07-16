from ...models import Candidate
import re

def check_s(text: str) -> Candidate | None:

    include_pattern = r'#include\s*[<"][^>"]+[>"]'
    include_found = re.search(include_pattern, text) is not None
    if include_found:
        return Candidate(
            media_type="text/x-c",
            extension="c",
            confidence=1.0,
            breakdown={"lang": "c"}
        )
    return None