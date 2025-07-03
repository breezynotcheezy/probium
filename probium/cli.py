from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .core import detect, _detect_file, scan_dir
from .google_magika import detect_magika, require_magika, magika_env_only
from .trid_multi import detect_with_trid
import time

def cmd_detect(ns: argparse.Namespace) -> None:
    """Detect a file or directory and emit JSON."""
    if ns.magika or magika_env_only():
        try:
            require_magika()
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return
    target = ns.path
    if target.is_dir():
        results: list[dict] = []
        scan_kwargs = dict(
            pattern=ns.pattern,
            workers=ns.workers,
            cap_bytes=ns.capbytes,
            extensions=ns.ext,
            ignore=ns.ignore,
            no_cap=ns.nocap,
        )
        if ns.magika or magika_env_only():
            scan_kwargs["engine"] = "magika"
            scan_kwargs.pop("cap_bytes", None)
        else:
            scan_kwargs["only"] = ns.only

        for path, res in scan_dir(target, **scan_kwargs):
            entry = {"path": str(path), **res.model_dump()}
            if ns.trid:
                trid_res = _detect_file(path, engine="trid", cap_bytes=None)
                entry["trid"] = trid_res.model_dump()
            results.append(entry)
        json.dump(results, sys.stdout, indent=None if ns.raw else 2)
    else:
        if ns.trid:
            res_map = detect_with_trid(
                target,
                cap_bytes=ns.capbytes,
                only=None if (ns.magika or magika_env_only()) else ns.only,
                extensions=ns.ext,
            )
            out = {k: v.model_dump() for k, v in res_map.items()}
        else:
            if ns.magika or magika_env_only():
                res = detect_magika(target, cap_bytes=None)
            else:
                res = _detect_file(
                    target,
                    cap_bytes=ns.capbytes,
                    only=ns.only,
                    extensions=ns.ext,
                    no_cap=ns.nocap
                )
            out = res.model_dump()
        json.dump(out, sys.stdout, indent=None if ns.raw else 2)
    sys.stdout.write("\n")

def cmd_watch(ns: argparse.Namespace) -> None:
    """Watch a directory and print detection results for new files."""

    if ns.magika or magika_env_only():
        try:
            require_magika()
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return

    def _handle(path: Path, res) -> None:
        entry = {"path": str(path), **res.model_dump()}
        json.dump(entry, sys.stdout, indent=None if ns.raw else 2)
        sys.stdout.write("\n")
        sys.stdout.flush()

    print(f"Watching {ns.root}... Press Ctrl+C to stop", file=sys.stderr)
    from .watch import watch
    if not ns.root.exists():
        print(f"Path {ns.root} does not exist", file=sys.stderr)
        return
    try:
        wc = watch(
            ns.root,
            _handle,
            recursive=ns.recursive,
            only=None if (ns.magika or magika_env_only()) else ns.only,
            extensions=ns.ext,
            interval=ns.interval,
            magika=ns.magika or magika_env_only(),
        )
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        wc.stop()
        print("Stopped", file=sys.stderr)

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="probium", description="Content-type detector")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_det = sub.add_parser("detect", help="Detect a file or directory")
    p_det.add_argument("path", type=Path, help="File or directory path")
    p_det.add_argument("--pattern", default="**/*", help="Glob pattern for directories")
    p_det.add_argument("--workers", type=int, default=8, help="Thread-pool size")
    p_det.add_argument(
        "--ignore",
        nargs="+",
        metavar="DIR",
        help="Directory names to skip during scan",
    )
    _add_common_options(p_det)
    p_det.set_defaults(func=cmd_detect)

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
    p_watch.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Polling interval when watchdog is unavailable",
    )
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
    ap.add_argument("--capbytes", type=int, default=4096, help="Max number of bytes to scan (default = 4096)")
    ap.add_argument("--nocap", action="store_true", help="Removes limit on how many bytes to scan")
    ap.add_argument(
        "--magika",
        action="store_true",
        help="Use Google Magika exclusively for detection",
    )

def main() -> None:
    ns = _build_parser().parse_args()
    ns.func(ns)


if __name__ == "__main__":
    main()
