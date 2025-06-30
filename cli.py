from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .core import detect, detect_file, scan_dir
from .trid_multi import detect_with_trid

def cmd_detect(ns: argparse.Namespace) -> None:
    """Detect a file or scan a directory and emit JSON."""
    target = ns.path
    if target.is_dir():
        results: list[dict] = []
        for path, res in scan_dir(
            target,
            pattern=ns.pattern,
            workers=ns.workers,
            cap_bytes=None,
            only=ns.only,
            extensions=ns.ext,
            ignore=ns.ignore,
        ):
            entry = {"path": str(path), **res.model_dump()}
            if ns.trid:
                trid_res = detect_file(path, engine="trid", cap_bytes=None)
                entry["trid"] = trid_res.model_dump()
            results.append(entry)
        json.dump(results, sys.stdout, indent=None if ns.raw else 2)
    else:
        if ns.trid:
            res_map = detect_with_trid(
                target,
                cap_bytes=None,
                only=ns.only,
                extensions=ns.ext,
            )
            out = {k: v.model_dump() for k, v in res_map.items()}
        else:
            res = detect(
                target,
                cap_bytes=None,
                only=ns.only,
                extensions=ns.ext,
            )
            out = res.model_dump()
        json.dump(out, sys.stdout, indent=None if ns.raw else 2)
    sys.stdout.write("\n")



def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="probium", description="Content-type detector")
    sub = p.add_subparsers(dest="cmd", required=True)
    p_scan = sub.add_parser("detect", help="Detect a file or directory")
    p_scan.add_argument("path", type=Path, help="File or directory to process")
    p_scan.add_argument("--pattern", default="**/*", help="Glob pattern (directories)")
    p_scan.add_argument("--workers", type=int, default=8, help="Thread-pool size")
    p_scan.add_argument(
        "--ignore",
        nargs="+",
        metavar="DIR",
        help="Directory names to skip during scan",
    )
    _add_common_options(p_scan)
    p_scan.set_defaults(func=cmd_detect)




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
    ap.add_argument("--trid", action="store_true", help="Include TRiD engine")



def main() -> None:
    ns = _build_parser().parse_args()
    ns.func(ns)


if __name__ == "__main__":
    main()
