"""High performance detection using custom magic numbers."""
from __future__ import annotations
from pathlib import Path

from .models import Result
from .cache import get as cache_get
from .registry import get_instance

# tuples of (signature bytes, offset, engine name)
MAGIC_SIGNATURES: list[tuple[bytes, int, str]] = [
    (b"MZ", 0, "exe"),
    (b"%PDF", 0, "pdf"),
    (b"\x89PNG\r\n\x1a\n", 0, "png"),
    (b"GIF87a", 0, "image"),
    (b"GIF89a", 0, "image"),
    (b"\xff\xd8\xff", 0, "image"),
    (b"ftyp", 4, "mp4"),
    (b"ID3", 0, "mp3"),
    (b"OggS", 0, "ogg"),
    (b"fLaC", 0, "flac"),
    (b"RIFF", 0, "wav"),
    (b"\x1f\x8b", 0, "gzip"),
    (b"BZh", 0, "bzip2"),
    (b"7z\xBC\xAF\x27\x1C", 0, "7z"),
    (b"\xFD7zXZ\x00", 0, "xz"),
    (b"Rar!", 0, "rar"),
    (b"BM", 0, "bmp"),
    (b"\x00\x00\x01\x00", 0, "ico"),
    (b"SQLite format 3\x00", 0, "sqlite"),
    (b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1", 0, "legacyoffice"),
    (b"PK\x03\x04", 0, "zipoffice"),
    (b"ustar", 257, "tar"),
    (b"<?xml", 0, "xml"),
]

_MAX_SCAN = max(off + len(sig) for sig, off, _ in MAGIC_SIGNATURES) + 1


def _load_bytes(source: str | Path | bytes, cap: int | None) -> bytes:
    if isinstance(source, (str, Path)):
        p = Path(source)
        cached = cache_get(p)
        if isinstance(cached, (bytes, bytearray)):
            return cached[:cap] if cap else bytes(cached)
        data = p.read_bytes() if cap is None else p.read_bytes()[:cap]
        return data
    return source[:cap] if cap else source


def detect_magic(source: str | Path | bytes, *, cap_bytes: int | None = None) -> Result:
    """Detect using custom magic signatures, falling back to normal detection."""
    payload = _load_bytes(source, cap_bytes or _MAX_SCAN)
    for sig, off, engine in MAGIC_SIGNATURES:
        end = off + len(sig)
        if len(payload) >= end and payload[off:end] == sig:
            return get_instance(engine)(payload)
    # fallback to standard autodetection
    from .core import detect
    return detect(payload if isinstance(source, (bytes, bytearray)) else source, cap_bytes=cap_bytes)
