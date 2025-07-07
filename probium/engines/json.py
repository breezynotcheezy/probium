from __future__ import annotations
import json
import re
import logging
import mimetypes
from ..scoring import score_tokens, score_magic
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()


@register
class JSONEngine(EngineBase):
    name = "json"
    #Identifier for this engine

    #Estimated cost to run this engine (used for prioritization or budgeting)

    cost = 0.05

    _TOKEN_RE = re.compile(r'[{}\[\]":,]')
    #these are not magic number sigs, "_MAGIC" field is used as placeholding binary sig. (delimiter replacement)
    _MAGIC = [b'{', b'[']

    # limit bytes inspected for expensive regex operations
    SAMPLE_SIZE = 65536

    def _make_result(
        self,
        conf: float,
        token_ratio: float,
        partial: bool = False,
        *,
        magic_len: int | None = None,
    ) -> Result:
        """Helper to build a :class:`Result` object."""

        breakdown = {"token_ratio": round(token_ratio, 3), "partial": partial}
        if magic_len is not None:
            breakdown["magic_len"] = float(magic_len)

        cand = Candidate(
            media_type="application/json",
            extension="json",
            confidence=conf,

            breakdown=breakdown,

        )
        return Result(candidates=[cand])

    def _find_json_fragment(self, text: str) -> str | None:
        """Return the first valid JSON snippet inside ``text`` if present."""

        decoder = json.JSONDecoder()
        snippet = text[: self.SAMPLE_SIZE]
        for match in re.finditer(r"[\{\[]", snippet):
            start = match.start()
            try:
                obj, idx = decoder.raw_decode(snippet[start:])
                end = start + idx
                return snippet[start:end]
            except Exception:
                continue
        return None

    def sniff(self, payload: bytes) -> Result:

        """Detect JSON using libmagic, magic bytes and structural analysis."""

        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover - rare
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime and "json" in mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or "json"
                    cand = Candidate(
                        media_type=mime,
                        extension=ext,
                        confidence=score_tokens(1.0),
                        breakdown={"token_ratio": 1.0, "libmagic": True},
                    )
                    return Result(candidates=[cand])


        try:
            text = payload.decode("utf-8")
        except Exception:
            return Result(candidates=[])


        stripped = text.lstrip()
        magic_hit = None
        for m in self._MAGIC:
            if stripped.startswith(m.decode("latin1")):
                magic_hit = m
                break


        text = text.strip()
        if not text:
            return Result(candidates=[])

        sample = text[: self.SAMPLE_SIZE]
        try:
            json.loads(text)
            parse_ok = True
        except Exception:
            parse_ok = False

        token_count = len(self._TOKEN_RE.findall(sample))
        token_ratio = token_count / max(len(sample), 1)

        if parse_ok:
            conf = score_tokens(1.0)
            if magic_hit:
                conf = max(conf, score_magic(len(magic_hit)))
            return self._make_result(conf, token_ratio, magic_len=len(magic_hit) if magic_hit else None)
        # full parse failed, attempt partial analysis

        frag = self._find_json_fragment(sample)
        if frag is not None:
            try:
                json.loads(frag)
                conf = score_tokens(min(0.9, token_ratio))
                if magic_hit:
                    conf = max(conf, score_magic(len(magic_hit)))
                return self._make_result(conf, token_ratio, partial=True, magic_len=len(magic_hit) if magic_hit else None)

            except Exception:
                pass

        if token_ratio > 0.3 and ":" in text:
            conf = score_tokens(min(token_ratio, 0.8))

            if magic_hit:
                conf = max(conf, score_magic(len(magic_hit)))
            return self._make_result(conf, token_ratio, partial=True, magic_len=len(magic_hit) if magic_hit else None)


        return Result(candidates=[])
