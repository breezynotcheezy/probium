from __future__ import annotations
import argparse
import json
import sys
import os
import asyncio
from pathlib import Path
from .core import detect, _detect_file, scan_dir

from .google_magika import detect_magika, require_magika

from .trid_multi import detect_with_trid
import time

# ANSI color codes for selected file extensions
COLOR_MAP = {
    "csv": "\033[32m",  # green
    "pdf": "\033[91m",  # light red
    "doc": "\033[94m",  # light blue
    "docx": "\033[94m",
    "png": "\033[95m",  # pink (magenta)
}
RESET = "\033[0m"


def _colorize_path(path: Path) -> str:
    """Return the path string wrapped in ANSI color codes if known."""
    ext = path.suffix.lower().lstrip(".")
    color = COLOR_MAP.get(ext)
    if color:
        return f"{color}{path}{RESET}"
    return str(path)

def cmd_detect(ns: argparse.Namespace) -> None:
    """Detect a file or directory and emit JSON."""
    start_total = time.perf_counter()
    if ns.magika:
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
            processes=ns.processes,
            cap_bytes=ns.capbytes,
            extensions=ns.ext,
            ignore=ns.ignore,
            no_cap=ns.nocap,
        )
        if ns.magika:
            scan_kwargs["engine"] = "magika"
            scan_kwargs.pop("cap_bytes", None)
        else:
            scan_kwargs["only"] = ns.only


        if ns.ndjson:
            write = sys.stdout.write
            dump = lambda e: json.dump(e, sys.stdout, indent=None if ns.raw else 2)
            if ns.sync:

                for path, res in scan_dir(target, cache=not ns.no_cache, **scan_kwargs):

                    entry = {"path": str(path), **res.model_dump()}
                    if ns.color:
                        entry["path"] = _colorize_path(path)
                    if ns.trid:

                        trid_res = _detect_file(path, engine="trid", cap_bytes=None, cache=not ns.no_cache)

                        entry["trid"] = trid_res.model_dump()
                    dump(entry)
                    write("\n")
                    sys.stdout.flush()
            else:
                async def _run() -> None:
                    from .core import scan_dir_async

                    async for path, res in scan_dir_async(target, cache=not ns.no_cache, **scan_kwargs):

                        entry = {"path": str(path), **res.model_dump()}
                        if ns.color:
                            entry["path"] = _colorize_path(path)
                        if ns.trid:

                            trid_res = _detect_file(path, engine="trid", cap_bytes=None, cache=not ns.no_cache)

                            entry["trid"] = trid_res.model_dump()
                        dump(entry)
                        write("\n")
                        sys.stdout.flush()

                asyncio.run(_run())
        else:
            if ns.sync:

                for path, res in scan_dir(target, cache=not ns.no_cache, **scan_kwargs):

                    entry = {"path": str(path), **res.model_dump()}
                    if ns.color:
                        entry["path"] = _colorize_path(path)
                    if ns.trid:

                        trid_res = _detect_file(path, engine="trid", cap_bytes=None, cache=not ns.no_cache)
                        entry["trid"] = trid_res.model_dump()
                    results.append(entry)
            else:
                async def _run() -> None:
                    from .core import scan_dir_async
                    async for path, res in scan_dir_async(target, cache=not ns.no_cache, **scan_kwargs):

                        entry = {"path": str(path), **res.model_dump()}
                        if ns.color:
                            entry["path"] = _colorize_path(path)
                        if ns.trid:

                            trid_res = _detect_file(path, engine="trid", cap_bytes=None, cache=not ns.no_cache)

                            entry["trid"] = trid_res.model_dump()
                        results.append(entry)

                asyncio.run(_run())
            json.dump(results, sys.stdout, indent=None if ns.raw else 2)

    else:
        if ns.trid:
            res_map = detect_with_trid(
                target,
                cap_bytes=ns.capbytes,
                only=None if ns.magika else ns.only,
                extensions=ns.ext,
                cache=not ns.no_cache,
            )
            out = {k: v.model_dump() for k, v in res_map.items()}
        else:
            if ns.magika:
                res = detect_magika(target, cap_bytes=None)
            else:
                res = _detect_file(
                    target,
                    cap_bytes=ns.capbytes,
                    only=ns.only,
                    extensions=ns.ext,
                    no_cap=ns.nocap,
                    cache=not ns.no_cache,
                )
            out = res.model_dump()
        if ns.color:
            out["path"] = _colorize_path(target)
        json.dump(out, sys.stdout, indent=None if ns.raw else 2)
    sys.stdout.write("\n")
    if ns.benchmark:
        total_ms = (time.perf_counter() - start_total) * 1000
        print(f"Total time: {total_ms:.1f} ms", file=sys.stderr)

def cmd_watch(ns: argparse.Namespace) -> None:
    """Watch a directory and print detection results for new files."""

    if ns.magika:
        try:
            require_magika()
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return

    def _handle(path: Path, res) -> None:
        entry = {"path": str(path), **res.model_dump()}
        if ns.color:
            entry["path"] = _colorize_path(path)
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
            only=None if ns.magika else ns.only,
            extensions=ns.ext,
            interval=ns.interval,
            magika=ns.magika,
            cache=not ns.no_cache,
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
    p_det.add_argument(
        "--workers",
        type=int,
        default=os.cpu_count() or 4,
        help="Thread-pool size (default: CPU count)",
    )

    p_det.add_argument(
        "--processes",
        type=int,
        default=0,
        help="Use a process pool with this many workers",
    )

    p_det.add_argument(
        "--ignore",
        nargs="+",
        metavar="DIR",
        help="Directory names to skip during scan",
    )
    p_det.add_argument(
        "--benchmark",
        action="store_true",
        help="Print total runtime to stderr",
    )
    p_det.add_argument(
        "--sync",
        action="store_true",
        help="Use synchronous scanning instead of asyncio",
    )

    p_det.add_argument(
        "--ndjson",
        action="store_true",
        help="Stream newline-delimited JSON results",
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
    ap.add_argument(
        "--no-cache",
        dest="no_cache",
        action="store_true",
        help="Disable result caching",
    )
    ap.add_argument(
        "--color",
        action="store_true",
        help="Colorize path values based on file type",
    )

def main() -> None:
    ns = _build_parser().parse_args()
    ns.func(ns)


if __name__ == "__main__":
    main()
