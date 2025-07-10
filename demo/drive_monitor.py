#!/usr/bin/env python3
"""Monitor for new drives and scan them with Probium."""
from __future__ import annotations
import time
from pathlib import Path
import psutil
from probium import scan_dir

checked = {p.mountpoint for p in psutil.disk_partitions(all=False)}


def scan_drive(mount: str) -> None:
    print(f"Scanning drive {mount}...")
    for path, result in scan_dir(mount, workers=2):
        cand = result.candidates[0] if result.candidates else None
        if cand:
            print(f"{path} -> {cand.media_type}")
        if Path(path).suffix.lower().lstrip(".") in {"exe", "bat", "bad"}:
            print("*** VIRUS DETECTED! ***")


def main() -> None:
    print("Waiting for new drives... Press Ctrl+C to stop.")
    while True:
        current = {p.mountpoint for p in psutil.disk_partitions(all=False)}
        new_drives = current - checked
        for mount in new_drives:
            print(f"Drive detected: {mount}")
            scan_drive(mount)
            checked.add(mount)
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting")
