from __future__ import annotations

import asyncio
import concurrent.futures as cf
import functools
import logging
import os
from pathlib import Path
from typing import Any, Iterable, Sequence

# directories ignored by default when scanning
DEFAULT_IGNORES = {".git", "venv", ".venv", "__pycache__"}
from .cache import get as cache_get, put as cache_put
from .registry import list_engines, get_instance
from .magic_service import MAGIC_SIGNATURES, _MAX_SCAN
from .scoring import score_magic

from .models import Result, Candidate

logger = logging.getLogger(__name__)


def _load_bytes(source: str | Path | bytes, cap: int | None) -> bytes:
    """Return raw bytes, never a Result (guards against cache mix-ups)."""
    if cap is not None and cap < 0:
        cap = None

    if isinstance(source, (str, Path)):
        p = Path(source)
        if not p.exists():
            # logger.warning(f"Source file does not exist: {p}")
            return b""
        cached = cache_get(p)
        if isinstance(cached, (bytes, bytearray)):
            return cached[:cap] if cap else bytes(cached)
        try:
            with p.open("rb") as fh:
                if cap is None:
                    data = fh.read()
                else:
                    data = fh.read(cap)
            return data
        except Exception:
            # logger.error(f"Failed to read file {p}: {e}")
            return b""
    return source[:cap] if (cap is not None) else source


def _detect_file(
    source: str | Path | bytes,
    engine: str = "auto",
    *,
    cap_bytes: int | None = 4096,
    engine_order: Iterable[str] | None = None,
    only: Iterable[str] | None = None,
    extensions: Iterable[str] | None = None,
    no_cap: bool = False,
    cache: bool = True,
) -> Result:
    """Identify ``source`` using registered engines.

    This low-level helper processes a single file or byte sequence. Use
    :func:`detect` for auto-detection of paths that may be directories.

    Parameters
    ----------
    source:
        File path, bytes or byte-like object to inspect.
    engine:
        Force the use of a single engine instead of autodetecting.
    cap_bytes:
        Read at most this many bytes from ``source``.
    engine_order:
        Optional explicit engine sequence to try.
    only:
        Restrict autodetection to this iterable of engine names.

    extensions:
        Optional iterable of file extensions to allow when ``source`` is a
        path. Detection is skipped if the extension is not listed.


    cache:
        Whether to store and retrieve results from the cache.
    """

    if cap_bytes is not None and cap_bytes < 0:
        cap_bytes = None

    if extensions is not None and isinstance(source, (str, Path)):
        allowed = {e.lower().lstrip(".") for e in extensions}
        suffix = Path(source).suffix.lower().lstrip(".")
        if suffix and suffix not in allowed:
            return Result(
                candidates=[
                    Candidate(media_type="application/octet-stream", confidence=0.0)
                ]
            )

    p: Path | None = None
    if isinstance(source, (str, Path)):
        p = Path(source)
        if not p.exists():
            return Result(
                candidates=[
                    Candidate(media_type="application/x-missing", confidence=0.0)
                ],
                error=f"File or Directory does not exist: {p}",
            )
        if p.is_dir():
            return Result(
                candidates=[Candidate(media_type="inode/directory", confidence=1.0)]
            )
        if cache:
            cached = cache_get(p)
            if isinstance(cached, Result):
                return cached

    ext = Path(source).suffix.lower().lstrip(".")
    if ext in {
        "docx",
        "docm",
        "pptx",
        "pptm",
        "xlsx",
        "xlsm",
        "xltx",
        "odt",
        "odp",
        "ods",
        "zip",
        "jar",
        "doc",
        "ppt",
        "xls",
    }:
        cap_bytes = min(8192, cap_bytes or 8192)

    if ext in {"ppt"}:
        no_cap = True

    scan_cap = cap_bytes
    if engine == "auto" and only is None:
        scan_cap = max(cap_bytes or 0, _MAX_SCAN)

    if no_cap:
        payload = _load_bytes(source, None)
    else:
        payload = _load_bytes(source, scan_cap)

    if engine != "auto":
        return get_instance(engine)(payload)

    if only is not None:
        only_list = list(only)
        if len(only_list) == 1:
            res = get_instance(only_list[0])(payload)
            if cache and isinstance(source, (str, Path)):
                cache_put(Path(source), res)
            return res

    magic_best: Result | None = None

    if only is not None:
        if engine_order is not None:
            allowed = set(only)
            engines = [e for e in engine_order if e in allowed]
        else:
            engines = list(only)
    else:
        engines = engine_order or list_engines()
        for sig, off, en in MAGIC_SIGNATURES:
            end = off + len(sig)
            if len(payload) >= end and payload[off:end] == sig:
                res = get_instance(en)(payload)
                if res.candidates:
                    res.candidates[0].breakdown = {"magic_len": float(len(sig))}
                    # res.candidates[0].confidence = score_magic(len(sig))
                    magic_best = res
                    if res.candidates[0].confidence >= 0.9:
                        return res
                break

    best: Result | None = magic_best

    for name in engines:
        res = get_instance(name)(payload)
        if res.candidates:
            if (
                best is None
                or res.candidates[0].confidence > best.candidates[0].confidence
            ):
                best = res
                if res.candidates[0].confidence >= 0.99:
                    break
    if (
        (best is None or best.candidates[0].confidence == 0.0)
        and cap_bytes is not None
        and isinstance(source, (str, Path))
    ):
        payload = Path(source).read_bytes()[:scan_cap]
        for name in engines:
            res = get_instance(name)(payload)
            if res.candidates:
                best = res
                break

    if best is None:
        best = Result(
            candidates=[
                Candidate(media_type="application/octet-stream", confidence=0.0)
            ]
        )
    if cache and isinstance(source, (str, Path)):
        cache_put(Path(source), best)
    return best


def detect(
    source: str | Path | bytes,
    *,
    pattern: str = "**/*",
    workers: int = os.cpu_count() or 4,
    ignore: Iterable[str] | None = None,
    **kw,
) -> Result | Iterable[tuple[Path, Result]]:
    """Detect a single file or recursively scan a directory.

    If ``source`` is a directory path, this function yields ``(path, Result)``
    tuples for each entry, delegating to :func:`scan_dir`. Otherwise a single
    :class:`Result` is returned.
    """

    if isinstance(source, (str, Path)) and Path(source).is_dir():
        return scan_dir(source, pattern=pattern, workers=workers, ignore=ignore, **kw)

    return _detect_file(source, **kw)


try:
    import anyio as _anyio
    from functools import partial

    async def detect_async(source: Any, **kw) -> Result:
        """Asynchronously call :func:`detect` in a worker thread.

        Parameters and return value are identical to :func:`detect`. The
        implementation uses ``anyio.to_thread`` when the optional ``anyio``
        package is installed. ``anyio.to_thread.run_sync`` does not forward
        keyword arguments, so we wrap the call with ``functools.partial`` to
        ensure ``detect`` receives them.
        """

        return await _anyio.to_thread.run_sync(partial(_detect_file, source, **kw))

except ImportError:  # pragma: no cover - optional dependency
    import asyncio

    async def detect_async(source: Any, **kw) -> Result:
        """Fallback asyncio-based implementation of :func:`detect_async`."""

        return await asyncio.to_thread(_detect_file, source, **kw)


def scan_dir(
    root: str | Path,
    *,
    pattern: str = "**/*",
    workers: int = os.cpu_count() or 4,
    processes: int = 0,
    only: Iterable[str] | None = None,
    extensions: Iterable[str] | None = None,
    ignore: Iterable[str] | None = None,
    **kw,
):
    """Yield ``(path, Result)`` tuples for files under ``root``.

    Parameters
    ----------
    root:
        Directory to scan.
    pattern:
        Glob pattern relative to ``root``.
    workers:
        Thread pool size for concurrent scanning.
    only:
        Restrict autodetection to this iterable of engine names.

    extensions:
        Optional iterable of file extensions to scan. Files with other
        extensions are skipped.

    ignore:
        Optional iterable of directory names to skip during scanning. If not
        provided, a default set of common build and VCS directories is ignored.


    kw:
        Additional arguments passed to :func:`detect`.
    """

    root = Path(root)

    if not root.exists() or not root.is_dir():
        # Simulate detect-style failure result
        yield root, Result(
            candidates=[
                Candidate(
                    media_type="application/x-missing",
                    extension=None,
                    confidence=0.0,
                )
            ],
            error=f"Path does not exist or is not a directory: {root}",
        )
        return

    ignore_set = set(DEFAULT_IGNORES)
    if ignore:
        ignore_set.update(Path(d).name for d in ignore)
    paths = []
    for p in root.glob(pattern):
        if ignore_set and any(part in ignore_set for part in p.relative_to(root).parts):
            continue
        paths.append(p)
    if extensions is not None:
        allowed = {e.lower().lstrip(".") for e in extensions}
        paths = [
            p
            for p in paths
            if p.is_dir() or not p.suffix or p.suffix.lower().lstrip(".") in allowed
        ]

    Executor = cf.ProcessPoolExecutor if processes > 0 else cf.ThreadPoolExecutor
    pool_size = processes if processes > 0 else workers
    with Executor(max_workers=pool_size) as ex:
        futs = {
            ex.submit(_detect_file, p, only=only, extensions=extensions, **kw): p
            for p in paths
        }

        for fut in cf.as_completed(futs):
            yield futs[fut], fut.result()


async def scan_dir_async(
    root: str | Path,
    *,
    pattern: str = "**/*",
    workers: int = os.cpu_count() or 4,
    processes: int = 0,
    only: Iterable[str] | None = None,
    extensions: Iterable[str] | None = None,
    ignore: Iterable[str] | None = None,
    **kw,
) -> Iterable[tuple[Path, Result]]:
    """Asynchronously yield ``(path, Result)`` for files and dirs under ``root``.

    Parameters are the same as :func:`scan_dir` but detection runs concurrently
    using ``asyncio`` tasks.
    """

    root = Path(root)
    ignore_set = set(DEFAULT_IGNORES)
    if ignore:
        ignore_set.update(Path(d).name for d in ignore)
    allowed = None
    if extensions is not None:
        allowed = {e.lower().lstrip(".") for e in extensions}

    paths = []
    for p in root.glob(pattern):
        if ignore_set and any(part in ignore_set for part in p.relative_to(root).parts):
            continue
        if allowed is not None and p.is_file():
            if p.suffix and p.suffix.lower().lstrip(".") not in allowed:
                continue
        paths.append(p)

    use_proc = processes > 0
    sem = asyncio.Semaphore(processes if use_proc else workers)
    executor: cf.Executor | None = None
    if use_proc:
        executor = cf.ProcessPoolExecutor(max_workers=processes)

    async def _run(path: Path):
        async with sem:
            if executor is not None:
                loop = asyncio.get_running_loop()
                res = await loop.run_in_executor(
                    executor,
                    functools.partial(
                        _detect_file,
                        path,
                        engine="auto",
                        cap_bytes=None,
                        only=only,
                        extensions=extensions,
                        **kw,
                    ),
                )
            else:
                res = await detect_async(path, only=only, extensions=extensions, **kw)
            return path, res

    tasks = [asyncio.create_task(_run(p)) for p in paths]
    for coro in asyncio.as_completed(tasks):
        yield await coro
    if executor is not None:
        executor.shutdown()
