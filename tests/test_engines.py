import io
import os
import gzip
import tarfile
import zipfile
import struct
import random
import pytest

from probium import detect


def _sample_pdf():
    return (
        b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n"
    )

def _sample_exe():
    return b"MZ" + b"\0" * 64

def _sample_gzip():
    return gzip.compress(b"hello world")

def _sample_png():
    return b"\x89PNG\r\n\x1a\n" + b"\0" * 10

def _sample_jpeg():
    return b"\xff\xd8\xff\xe0" + b"\0" * 10 + b"\xff\xd9"

def _sample_gif():
    return b"GIF89a" + b"\0" * 10

def _sample_mp3():
    return b"ID3" + b"\0" * 10

def _sample_mp4():
    return b"\x00\x00\x00\x18ftypisom" + b"\0" * 8

def _sample_wav():
    return b"RIFF" + b"\x24\x00\x00\x00" + b"WAVE" + b"\0" * 8

def _sample_tar():
    mem = io.BytesIO()
    with tarfile.open(fileobj=mem, mode="w") as tf:
        info = tarfile.TarInfo("test.txt")
        data = b"hello"
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
    return mem.getvalue()

def _sample_zip_office():
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w") as zf:
        zf.writestr("[Content_Types].xml", "")
        zf.writestr("word/document.xml", "")
    return mem.getvalue()

def _sample_legacy_office():
    return b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1" + b"\0" * 512

def _sample_html():
    return b"<html><body>hi</body></html>"

def _sample_json():
    return b"{\"a\":1}"

def _sample_xml():
    return b"<?xml version='1.0'?><r/>"

def _sample_text():
    return b"Just a plain text file.\n"

def _sample_sh():
    return b"#!/bin/sh\necho hi\n"

def _sample_bat():
    return b"@echo off\r\necho hi\r\n"

def _sample_fallback():
    return os.urandom(20)

BASE_SAMPLES = {
    "exe": _sample_exe(),
    "image": _sample_jpeg(),
    "mp3": _sample_mp3(),
    "sh": _sample_sh(),
    "xml": _sample_xml(),
    "fallback-engine": _sample_fallback(),
    "gzip": _sample_gzip(),
    "html": _sample_html(),
    "json": _sample_json(),
    "mp4": _sample_mp4(),
    "pdf": _sample_pdf(),
    "png": _sample_png(),
    "csv": b"a,b\n1,2\n3,4\n",  # simple csv
    "text": _sample_text(),
    "tar": _sample_tar(),
    "wav": _sample_wav(),
    "zipoffice": _sample_zip_office(),
    "legacyoffice": _sample_legacy_office(),
    "bat": _sample_bat(),
}


def _valid_variants(base: bytes) -> list[bytes]:
    return [base] * 5


def _invalid_variants(base: bytes) -> list[bytes]:
    # Prefix with a byte unlikely to match engine heuristics so random
    # payloads don't accidentally appear valid.
    return [b"\x00" + os.urandom(len(base) + i % 3) for i in range(10)]


def _cases():
    cases = []
    for engine, base in BASE_SAMPLES.items():
        valids = _valid_variants(base)
        invalids = _invalid_variants(base)
        for i, payload in enumerate(valids):
            cases.append((engine, payload, True, f"{engine}-ok-{i}"))
        for i, payload in enumerate(invalids):
            exp = engine == "fallback-engine"
            cases.append((engine, payload, exp, f"{engine}-bad-{i}"))
    return cases


_ALL_CASES = _cases()
_CASE_IDS = [case_id for _, _, _, case_id in _ALL_CASES]


@pytest.mark.parametrize(
    "engine,payload,expected,case_id", _ALL_CASES, ids=_CASE_IDS
)
def test_engines(engine: str, payload: bytes, expected: bool, case_id: str) -> None:
    res = detect(payload, engine=engine, cap_bytes=None)
    assert (len(res.candidates) > 0) == expected
