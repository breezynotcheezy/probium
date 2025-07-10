#!/usr/bin/env python3
"""Minimal anti-virus style demo using the Probium API."""
from __future__ import annotations
import argparse
from pathlib import Path
from probium import detect

SUSPICIOUS_EXTS = {"exe", "bat", "com", "bad"}


def scan_file(path: Path) -> None:
    res = detect(path)
    cand = res.candidates[0] if res.candidates else None
    if cand:
        print(f"{path} -> {cand.media_type} ({cand.extension})")
    if path.suffix.lower().lstrip(".") in SUSPICIOUS_EXTS:
        print(f"*** VIRUS DETECTED in {path}! ***")


def scan_dir(directory: Path) -> None:
    for p in directory.rglob("*"):
        if p.is_file():
            scan_file(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan a folder using Probium")
    parser.add_argument("path", type=Path, help="File or folder to scan")
    args = parser.parse_args()
    target = args.path
    if target.is_dir():
        scan_dir(target)
    else:
        scan_file(target)
