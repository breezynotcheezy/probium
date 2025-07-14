from __future__ import annotations
import string
from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
import re

@register
class TextEngine(EngineBase):
    name = "text"
    cost = 1.0

    def sniff(self, payload: bytes) -> Result:
        sample = payload[:512]
        try:
            text = sample.decode("utf-8")
        except UnicodeDecodeError:
            return Result(candidates=[])
        printable = set(string.printable)
        printable_count = sum(1 for c in text if c in printable or c in "\n\r\t")
        ratio = printable_count / max(len(text), 1)


        if ratio < 0.95:
            return Result(candidates=[])

        # Run detectors
        # check for languages with semicolons first
        if b';\x0D\x0A' in payload or b';\x0A' in payload:
            for checker in [self.check_java, self.check_javascript, self.check_cpp, self.check_rust]:
                result = checker(text)
                if result:
                    return Result(candidates=[result])
            cc = self.check_c(payload)
            if cc: return Result(candidates=[cc])

        for checker in [self.check_python, self.check_bat]:
            result = checker(text)
            if result:
                return Result(candidates=[result])

        # Default to plain text
        conf = score_tokens(ratio)
        cand = Candidate(
            media_type="text/plain",
            extension="txt",
            confidence=conf,
            breakdown={"token_ratio": ratio},
        )
        return Result(candidates=[cand])

        
        if ratio > 0.95 and "<" not in text and ">" not in text:
            conf = score_tokens(ratio)
            cand = Candidate(
                media_type="text/plain",
                extension="txt",
                confidence=conf,
                breakdown={"token_ratio": ratio},
            )
            return Result(candidates=[cand])

        return Result(candidates=[])
    
    def check_python(self, text: str) -> Candidate | None:
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

    def check_javascript(self, text: str) -> Candidate | None:
        keywords = ["let ", "var ", "console.log(", "=>"]
        if any(k in text for k in keywords):
            return Candidate(
                media_type="application/javascript",
                extension="js",
                confidence=1.0,
                breakdown={"lang": "javascript"}
            )
        return None

    def check_java(self, text: str) -> Candidate | None:
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
    
    def check_c(self, sample: bytes) -> Candidate | None:

        include_pattern = rb'#include\s*[<"][^>"]+[>"]'
        include_found = re.search(include_pattern, sample) is not None
        if include_found:
            return Candidate(
                media_type="text/x-c",
                extension="c",
                confidence=1.0,
                breakdown={"lang": "c"}
            )
        return None
    
    def check_cpp(self, text: str) -> Candidate | None:
        keywords = ["include <iostream>", "std::"]
        if any(k in text for k in keywords):
            return Candidate(
                media_type="text/x-c++",
                extension="cpp",
                confidence=1.0,
                breakdown={"lang": "c++"}
            )
        return None

    def check_bat(self, text: str) -> Candidate | None:
        patterns = [r"@echo\s+off", r"\brem\b"]
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            return Candidate(
                media_type="application/x-bat",
                extension="bat",
                confidence=1.0,
                breakdown={"lang": "batch"}
            )
        return None
    
    def check_rust(self, text: str) -> Candidate | None:
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

