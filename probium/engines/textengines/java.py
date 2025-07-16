from ...models import Candidate
import re

def check_s(text: str) -> Candidate | None:
    java_declaration_pattern = re.compile(
        r"\bpublic\s+(class|interface)\s+\w+(\s+(extends|implements)\s+\w+)?", re.MULTILINE
    )
    if java_declaration_pattern.search(text):
        return Candidate(
            media_type="text/x-java-source",
            extension="java",
            confidence=1.0,
            breakdown={"lang": "java", "match": "public class/interface declaration"}
        )
    keywords = ["public static void main(String", "System.out.println("]
    if any(k in text for k in keywords):
        return Candidate(
            media_type="text/x-java-source",
            extension="java",
            confidence=1.0,
            breakdown={"lang": "java"}
        )
    return None