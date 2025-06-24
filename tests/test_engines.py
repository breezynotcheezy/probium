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

def _sample_bmp():
    return b"BM" + b"\0" * 10

def _sample_flac():
    return b"fLaC" + b"\0" * 8

def _sample_ogg():
    return b"OggS" + b"\0" * 8

def _sample_rar():
    return b"Rar!" + b"\0" * 8

def _sample_xz():
    return b"\xFD7zXZ\x00" + b"\0" * 8

def _sample_bzip2():
    return b"BZh9" + b"\0" * 8

def _sample_7z():
    return b"7z\xBC\xAF\x27\x1C" + b"\0" * 8

def _sample_ico():
    return b"\x00\x00\x01\x00" + b"\0" * 8

def _sample_sqlite():
    return b"SQLite format 3\x00" + b"\0" * 8

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


def _sample_python():
    return b"#!/usr/bin/env python\nprint('hi')\n"

def _sample_java():
    return b"public class Test { public static void main(String[] a){ } }"

def _sample_c():
    return b"#include <stdio.h>\nint main(){return 0;}\n"

def _sample_js():
    return b"function test(){ console.log('hi'); }"

def _sample_ruby():
    return b"#!/usr/bin/env ruby\nputs 'hi'\n"

def _sample_rust():
    return b"fn main() { println!(\"hi\"); }"

def _sample_cpp():
    return b"#include <iostream>\nint main(){std::cout<<\"hi\";}"

def _sample_scala():
    return b"object Main extends App { println(\"hi\") }"

def _sample_go():
    return b"package main\nfunc main() { println(\"hi\") }"

def _sample_php():
    return b"<?php echo 'hi';"

def _sample_csharp():
    return b"using System; class P { static void Main(){ } }"

def _sample_perl():
    return b"#!/usr/bin/perl\nprint 'hi';\n"

def _sample_swift():
    return b"import Foundation\nfunc main(){print(\"hi\")}"

def _sample_kotlin():
    return b"fun main(){ println(\"hi\") }"

def _sample_haskell():
    return b"module Main where\nmain = putStrLn \"hi\""

def _sample_lua():
    return b"function main() print('hi') end"

def _sample_markdown():
    return b"# Title\n\nSome text"

def _sample_yaml():
    return b"key: value\nlist:\n  - item"

def _sample_ini():
    return b"[section]\nkey=value"

def _sample_makefile():
    return b"all:\n\techo hi"

def _sample_dockerfile():
    return b"FROM busybox\nCMD echo hi"

def _sample_terraform():
    return b"terraform { required_version=\"1.0\" }"

def _sample_toml():
    return b"[tool]\nname=\"hi\""

def _sample_powershell():
    return b"Write-Host 'hi'"

def _sample_clojure():
    return b"(ns hi) (defn -main [] (println \"hi\"))"

def _sample_elixir():
    return b"defmodule Hi do\nend"

def _sample_dart():
    return b"void main(){ print('hi'); }"

def _sample_zig():
    return b"pub fn main() void { std.debug.print(\"hi\", .{}); }"


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

    "bmp": _sample_bmp(),
    "flac": _sample_flac(),
    "ogg": _sample_ogg(),
    "rar": _sample_rar(),
    "xz": _sample_xz(),
    "bzip2": _sample_bzip2(),
    "7z": _sample_7z(),
    "ico": _sample_ico(),
    "sqlite": _sample_sqlite(),

    "python": _sample_python(),
    "java": _sample_java(),
    "c": _sample_c(),
    "js": _sample_js(),
    "ruby": _sample_ruby(),
    "rust": _sample_rust(),
    "cpp": _sample_cpp(),
    "scala": _sample_scala(),
    "go": _sample_go(),
    "php": _sample_php(),
    "csharp": _sample_csharp(),
    "perl": _sample_perl(),
    "swift": _sample_swift(),
    "kotlin": _sample_kotlin(),
    "haskell": _sample_haskell(),
    "lua": _sample_lua(),
    "markdown": _sample_markdown(),
    "yaml": _sample_yaml(),
    "ini": _sample_ini(),
    "makefile": _sample_makefile(),
    "dockerfile": _sample_dockerfile(),
    "terraform": _sample_terraform(),
    "toml": _sample_toml(),
    "powershell": _sample_powershell(),
    "clojure": _sample_clojure(),
    "elixir": _sample_elixir(),
    "dart": _sample_dart(),
    "zig": _sample_zig(),

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


def test_directory_detection(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    res = detect(d)
    assert res.candidates and res.candidates[0].media_type == "inode/directory"


def test_python_precedence():
    res = detect(BASE_SAMPLES["python"], cap_bytes=None)
    assert res.candidates
    assert res.candidates[0].media_type == "text/x-python"


def test_python_without_shebang():
    res = detect(b"def foo():\n    pass\n", cap_bytes=None)
    assert res.candidates
    assert res.candidates[0].media_type == "text/x-python"


def test_python_bytecode_detection():
    import importlib.util
    payload = importlib.util.MAGIC_NUMBER + b"\x00\x00\x00\x00"
    res = detect(payload, cap_bytes=None)
    assert res.candidates
    assert res.candidates[0].media_type == "application/x-python-bytecode"
