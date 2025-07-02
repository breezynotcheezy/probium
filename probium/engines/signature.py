from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register
import logging
import mimetypes
from ..libmagic import load_magic

logger = logging.getLogger(__name__)

_magic = load_magic()

# quick byte signature lookups for common formats
_SIGNATURES: dict[bytes, tuple[str, str]] = {
    b"\xFF\xD8\xFF": ("image/jpeg", "jpg"),
    b"\x89PNG\r\n\x1a\n": ("image/png", "png"),
    b"GIF87a": ("image/gif", "gif"),
    b"GIF89a": ("image/gif", "gif"),
    b"%PDF": ("application/pdf", "pdf"),
    b"PK\x03\x04": ("application/zip", "zip"),
    b"ID3": ("audio/mpeg", "mp3"),
    b"OggS": ("application/ogg", "ogx"),
    b"fLaC": ("audio/flac", "flac"),
    b"RIFF": ("audio/wav", "wav"),
    b"\x1f\x8b": ("application/gzip", "gz"),
    b"BZh": ("application/x-bzip", "bz2"),
    b"7z\xBC\xAF\x27\x1C": ("application/x-7z-compressed", "7z"),
    b"\xFD7zXZ\x00": ("application/x-xz", "xz"),
    b"Rar!": ("application/vnd.rar", "rar"),
    b"BM": ("image/bmp", "bmp"),
    b"\x00\x00\x01\x00": ("image/x-icon", "ico"),
    b"SQLite format 3\x00": ("application/vnd.sqlite3", "sqlite"),
}

_MAX_SIG_LEN = max(len(sig) for sig in _SIGNATURES)


@register
class SignatureEngine(EngineBase):
    """Detect types based on simple byte signatures."""

    name = "signature"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        if _magic is not None:
            try:
                mime = _magic.from_buffer(payload)
            except Exception as exc:  # pragma: no cover
                logger.warning("libmagic failed: %s", exc)
            else:
                if mime:
                    ext = (mimetypes.guess_extension(mime) or "").lstrip(".") or None
                    cand = Candidate(
                        media_type=mime,
                        extension=ext,
                        confidence=score_tokens(0),
                        breakdown={"token_ratio": 1.0},
                    )
                    return Result(candidates=[cand])

        head = payload[:_MAX_SIG_LEN]
        for sig, (mime, ext) in _SIGNATURES.items():
            if head.startswith(sig):
                cand = Candidate(
                    media_type=mime,
                    extension=ext,
                    confidence=score_magic(len(sig)),
                    breakdown={"magic_len": float(len(sig))},
                )
                return Result(candidates=[cand])
        return Result(candidates=[])
