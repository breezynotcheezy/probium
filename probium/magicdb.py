from __future__ import annotations

"""Simple magic number lookup used by multiple engines."""

from typing import Dict, Tuple

from .models import Candidate

# Map of file header bytes to (media type, extension)
FILE_SIGNATURES: Dict[bytes, Tuple[str, str]] = {
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

# Basic language shebang / opener patterns treated as magic numbers
LANG_SIGNATURES: Dict[bytes, Tuple[str, str]] = {
    b"#!/usr/bin/env python": ("text/x-python", "py"),
    b"#!/usr/bin/python": ("text/x-python", "py"),
    b"#!/usr/bin/env php": ("text/x-php", "php"),
    b"<?php": ("text/x-php", "php"),
    b"#!/usr/bin/env bash": ("text/x-shellscript", "sh"),
    b"#!/bin/bash": ("text/x-shellscript", "sh"),
    b"#!/usr/bin/env sh": ("text/x-shellscript", "sh"),
    b"#!/usr/bin/env node": ("application/javascript", "js"),
    b"#!/usr/bin/env perl": ("text/x-perl", "pl"),
    b"#!/usr/bin/env ruby": ("text/x-ruby", "rb"),
    b"#!/usr/bin/env powershell": ("text/x-powershell", "ps1"),
    b"#!/usr/bin/env swift": ("text/x-swift", "swift"),
    b"#!/usr/bin/env zig": ("text/x-zig", "zig"),
}

_MAX_SIG_LEN = max(max(len(k) for k in FILE_SIGNATURES), max(len(k) for k in LANG_SIGNATURES))


def match_magic(payload: bytes) -> Candidate | None:
    """Return a Candidate if ``payload`` matches a known signature."""
    head = payload[:_MAX_SIG_LEN]
    for sig, (mime, ext) in FILE_SIGNATURES.items():
        if head.startswith(sig):
            return Candidate(media_type=mime, extension=ext, confidence=0.99)
    for sig, (mime, ext) in LANG_SIGNATURES.items():
        if head.startswith(sig):
            return Candidate(media_type=mime, extension=ext, confidence=0.99)
    return None
