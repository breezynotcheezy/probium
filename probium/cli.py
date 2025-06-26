from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .core import detect, scan_dir
from .trid_multi import detect_with_trid
from .watch import watch
import time

def cmd_one(ns: argparse.Namespace) -> None:
    """Detect a single file and emit JSON."""
    if ns.trid:
        res_map = detect_with_trid(
            ns.file,
            cap_bytes=None,
            only=ns.only,
            extensions=ns.ext,
        )
        out = {k: v.model_dump() for k, v in res_map.items()}
    else:
        res = detect(
            ns.file,
            cap_bytes=None,
            only=ns.only,
            extensions=ns.ext,
        )
        out = res.model_dump()
    json.dump(out, sys.stdout, indent=None if ns.raw else 2)
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
        entry = {"path": str(path), **res.model_dump()}
        if ns.trid:
            trid_res = detect(path, engine="trid", cap_bytes=None)
            entry["trid"] = trid_res.model_dump()
        results.append(entry)

    json.dump(results, sys.stdout, indent=None if ns.raw else 2)
    sys.stdout.write("\n")


def cmd_watch(ns: argparse.Namespace) -> None:
    """Watch a directory and print detection results for new files."""

    def _handle(path: Path, res) -> None:
        entry = {"path": str(path), **res.model_dump()}
        json.dump(entry, sys.stdout, indent=None if ns.raw else 2)
        sys.stdout.write("\n")
        sys.stdout.flush()

    print(f"Watching {ns.root}... Press Ctrl+C to stop", file=sys.stderr)
    wc = watch(
        ns.root,
        _handle,
        recursive=ns.recursive,
        only=ns.only,
        extensions=ns.ext,
    )
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        wc.stop()
        print("Stopped", file=sys.stderr)



def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="probium", description="Content-type detector")
    sub = p.add_subparsers(dest="cmd", required=True)
    p_one = sub.add_parser("one", help="Detect a single file")
    p_one.add_argument("file", type=Path, help="Path to file")
    _add_common_options(p_one)
    p_one.set_defaults(func=cmd_one)


    # all
    p_all = sub.add_parser("all", help="Scan directory")
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

    # watch
    p_watch = sub.add_parser("watch", help="Monitor directory for new files")
    p_watch.add_argument("root", type=Path, help="Root folder")
    p_watch.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Do not watch subdirectories",
    )
    p_watch.set_defaults(recursive=True)
    _add_common_options(p_watch)
    p_watch.set_defaults(func=cmd_watch)
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
