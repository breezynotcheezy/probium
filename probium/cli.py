#hashing
import json
import sys
import argparse
from pathlib import Path
from .core import detect, scan_dir
def cmd_one(args: argparse.Namespace) -> None:

    res = detect(args.file, cap_bytes=None, only=args.only, extensions=args.ext)

    res = detect(args.file, cap_bytes=None, only=args.only)

    json.dump(res.model_dump(), sys.stdout, indent=None if args.raw else 2)
    sys.stdout.write("\n")
def cmd_all(args: argparse.Namespace) -> None:
    results = []
    for path, res in scan_dir(
        args.root,
        pattern=args.pattern,
        workers=args.workers,
        cap_bytes=None,
        only=args.only,

        extensions=args.ext,

    ):
        line = {"path": str(path), **res.model_dump()}
        results.append(line)
    json.dump(results, sys.stdout, indent=None if args.raw else 2)
    sys.stdout.write("\n")
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fastback", description="fastback one|all")
    sub = p.add_subparsers(dest="cmd", required=True)
    p_one = sub.add_parser("one", help="Detect a single file")
    p_one.add_argument("file", type=Path, help="Path to file")
    p_one.add_argument(
        "--only",
        nargs="+",
        metavar="ENGINE",
        help="Restrict detection to these engines",
    )
    p_one.add_argument(
        "--ext",
        nargs="+",
        metavar="EXT",
        help="Only analyze files with these extensions",
    )
    p_one.add_argument("--raw", action="store_true", help="compact JSON")
    p_one.set_defaults(func=cmd_one)
    p_all = sub.add_parser("all", help="Scan directory recursively")
    p_all.add_argument("root", type=Path, help="root folder")
    p_all.add_argument("--pattern", default="**/*", help="glob (default **/*)")
    p_all.add_argument("--workers", type=int, default=8, help="thread pool size")
    p_all.add_argument(
        "--only",
        nargs="+",
        metavar="ENGINE",
        help="Restrict detection to these engines",
    )

    p_all.add_argument(
        "--ext",
        nargs="+",
        metavar="EXT",
        help="Only analyze files with these extensions",
    )


    p_all.add_argument("--raw", action="store_true", help="compact JSON")
    p_all.set_defaults(func=cmd_all)
    return p
def main() -> None:
    args = build_parser().parse_args()
    args.func(args)
if __name__ == "__main__":
    main()
