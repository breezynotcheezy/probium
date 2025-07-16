from __future__ import annotations
import string
from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
import re
import os
import importlib
import chardet

@register
class TextEngine(EngineBase):
    name = "text"
    cost = 1.0

    def __init__(self):
        super().__init__()
        self.checkers = self.load_language_checkers()


    def sniff(self, payload: bytes) -> Result:
        sample = payload[:512]
        text = "\x00"
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            if chardet:
                res = chardet.detect(sample)
                encoding = res.get("encoding")
                #print(encoding)
                if encoding:
                    try:
                        text = sample.decode(encoding)
                    except:
                        return Result(candidates=[])
            else:
                return Result(candidates=[])
            
        printable = set(string.printable)
        printable_count = sum(1 for c in text if c in printable or c in "\n\r\t")
        ratio = printable_count / max(len(text), 1)
        
        if ratio < 0.8:
            return Result(candidates=[])

        # check csv and xml
        if "<" in text:
            for checker in self.checkers["xml"]:
                    result = checker(text=text, payload=payload)
                    if result:
                        return Result(candidates=[result])

        # Run detectors
        # check for languages with semicolons first
        if b';\x0D\x0A' in payload or b';\x0A' in payload:
            for checker in self.checkers["colon"]:
                result = checker(text)
                if result:
                    return Result(candidates=[result])

        # check json        
        if text.startswith("{") or text.startswith("["):
            for checker in self.checkers["json"]:
                result = checker(text)
                if result:
                    return Result(candidates=[result])


           
        for checker in self.checkers["csv"]:
                result = checker(text=text)
                if result:
                    return Result(candidates=[result])
            
        # check remaining
        for checker in self.checkers["standard"]:
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

    


    def load_language_checkers(self):
        """Dynamically imports all modules in the additionalengines folder with a `check` function."""
        checkers = {"standard": [], "colon": [], "json": [], "xml": [], "csv": []}

        dir_path = os.path.dirname(__file__)
        additional_path = os.path.join(dir_path, "textengines")
        for file in os.listdir(additional_path):
            if file.endswith(".py") and not file.startswith("_"):
                mod_name = file[:-3]
                try:
                    mod = importlib.import_module(f".textengines.{mod_name}", package=__package__)
                    if hasattr(mod, "check"):
                        checkers["standard"].append(mod.check)

                    if hasattr(mod, "check_s"):
                        checkers["colon"].append(mod.check_s)

                    if hasattr(mod, "check_json"):
                        checkers["json"].append(mod.check_json)

                    if hasattr(mod, "check_csv"):
                        checkers["csv"].append(mod.check_csv)
                    
                    # xml commented out for now
                    
                    if hasattr(mod, "check_xml"):
                        checkers["xml"].append(mod.check_xml)
                    
                except Exception as e:
                    print(f"Failed to load {mod_name}: {e}")
        return checkers
