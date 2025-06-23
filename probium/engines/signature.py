from __future__ import annotations

from ..models import Candidate, Result
from .base import MagicEngine
from ..registry import register
import logging

logger = logging.getLogger(__name__)


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
class SignatureEngine(MagicEngine):
    """Detect types based on simple byte signatures."""

    name = "signature"
    cost = 0.05

    magic_hint = ""

    def sniff(self, payload: bytes) -> Result:
        res = self._probe_magic(payload)
        if res:
            return res

        head = payload[:_MAX_SIG_LEN]
        for sig, (mime, ext) in _SIGNATURES.items():
            if head.startswith(sig):
                cand = Candidate(media_type=mime, extension=ext, confidence=0.99)
                return Result(candidates=[cand])
        return Result(candidates=[])
