from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .core import detect, scan_dir

def cmd_one(ns: argparse.Namespace) -> None:
    """Detect a single file and emit JSON."""
    res = detect(
        ns.file,
        cap_bytes=None,
        only=ns.only,
        extensions=ns.ext,
    )
    json.dump(res.model_dump(), sys.stdout, indent=None if ns.raw else 2)
    sys.stdout.write("\n")


def cmd_all(ns: argparse.Namespace) -> None:
    """Walk a directory, run detection on each file, emit one big JSON list."""
    results: list[dict] = []
    for path, res in scan_dir(
        ns.root,
        pattern=ns.pattern,
        workers=ns.workers,
        cap_bytes=None,
        only=ns.only,
        extensions=ns.ext,
        ignore=ns.ignore,
    ):

        results.append({"path": str(path), **res.model_dump()})

    json.dump(results, sys.stdout, indent=None if ns.raw else 2)
    sys.stdout.write("\n")



def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="probium", description="Content-type detector")
    sub = p.add_subparsers(dest="cmd", required=True)
    p_one = sub.add_parser("one", help="Detect a single file")
    p_one.add_argument("file", type=Path, help="Path to file")
    _add_common_options(p_one)
    p_one.set_defaults(func=cmd_one)


    # all 
    p_all = sub.add_parser("all", help="Scan directory recursively")
    p_all.add_argument("root", type=Path, help="Root folder")
    p_all.add_argument("--pattern", default="**/*", help="Glob pattern (default **/*)")
    p_all.add_argument("--workers", type=int, default=8, help="Thread-pool size")
    p_all.add_argument(
        "--ignore",
        nargs="+",
        metavar="DIR",
        help="Directory names to skip during scan",
    )
    _add_common_options(p_all)
    p_all.set_defaults(func=cmd_all)




    return p


def _add_common_options(ap: argparse.ArgumentParser) -> None:
    ap.add_argument(
        "--only",
        nargs="+",
        metavar="ENGINE",
        help="Restrict detection to these engines",
    )
    ap.add_argument(
        "--ext",
        nargs="+",
        metavar="EXT",
        help="Only analyse files with these extensions",
    )
    ap.add_argument("--raw", action="store_true", help="Emit compact JSON")



def main() -> None:
    ns = _build_parser().parse_args()
    ns.func(ns)


if __name__ == "__main__":
    main()
