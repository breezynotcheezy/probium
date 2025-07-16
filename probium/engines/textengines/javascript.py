from ...models import Candidate
import re

def check_s(text: str) -> Candidate | None:
    patterns = [
        r"\bfunction\s+\w+\s*\(",                 # function myFunc(
        r"\blet\s+\w+",                           # let variable
        r"\bvar\s+\w+",                           # var variable
        r"console\.log\s*\(",                     # console.log(...)
        r"=>",                                     # arrow function
        r"\bexport\s+(default\s+)?(function|class|const|let|var)?",  # export default ...
        r"\basync\s+function\s+\w*",              # async function
        r"\bawait\s+\w+",                         # await something
        r"\bdocument\.\w+",                       # document.querySelector etc.
        r"\bwindow\.\w+",                         # window.location etc.
        r"\bPromise\s*\.",                        # Promise.then, Promise.all, etc.
    ]

    if any(re.search(p, text) for p in patterns):
        if '<!DOCTYPE html' in text or '<!DOCTYPE HTML' in text or '<html' in text or '<HTML' in text or '<a href=' in text:
            return Candidate(
            media_type="text/html",
            extension="html",
            confidence=1.0,
            breakdown={"partial": True, "contains js": True}
        )
        return Candidate(
            media_type="application/javascript",
            extension="js",
            confidence=1.0,
            breakdown={"lang": "javascript", "matched": "js keyword or structure"}
        )
    return None