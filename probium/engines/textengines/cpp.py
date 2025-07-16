from ...models import Candidate
import re

def check_s(text: str) -> Candidate | None:
    keywords = ["include <iostream>", "std::"]
    if any(k in text for k in keywords):
        return Candidate(
            media_type="text/x-c++",
            extension="cpp",
            confidence=1.0,
            breakdown={"lang": "c++"}
        )
    return None