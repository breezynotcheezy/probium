from __future__ import annotations
import concurrent.futures as cf
import logging
import os
from pathlib import Path
from typing import Any, Iterable, Sequence

# directories ignored by default when scanning
DEFAULT_IGNORES = {".git", "venv", ".venv", "__pycache__"}
from .cache import get as cache_get, put as cache_put
from .registry import list_engines, get_instance
from .models import Result, Candidate
logger = logging.getLogger(__name__)
def _load_bytes(source: str | Path | bytes, cap: int | None) -> bytes:
    """Return raw bytes, never a Result (guards against cache mix-ups)."""
    if isinstance(source, (str, Path)):
        p = Path(source)
        cached = cache_get(p)
        if isinstance(cached, (bytes, bytearray)):
            return cached[:cap] if cap else bytes(cached)
        data = p.read_bytes() if cap is None else p.read_bytes()[:cap]
        return data
    return source[:cap] if cap else source
def detect(
    source: str | Path | bytes,
    engine: str = "auto",
    *,
    cap_bytes: int | None = 4096,
    engine_order: Iterable[str] | None = None,
    only: Iterable[str] | None = None,

    extensions: Iterable[str] | None = None,


    cache: bool = True,
) -> Result:
    """Identify ``source`` using registered engines.

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


    if extensions is not None and isinstance(source, (str, Path)):
        allowed = {e.lower().lstrip('.') for e in extensions}
        if Path(source).suffix.lower().lstrip('.') not in allowed:
            return Result(candidates=[Candidate(media_type="application/octet-stream", confidence=0.0)])



    p: Path | None = None
    if isinstance(source, (str, Path)):
        p = Path(source)
        if p.is_dir():
            return Result(candidates=[Candidate(media_type="inode/directory", confidence=1.0)])
    payload = _load_bytes(source, cap_bytes)

    if engine != "auto":
        return get_instance(engine)(payload)

    engines: Sequence[str] = engine_order or list_engines()
    if only is not None:
        allowed = set(only)
        engines = [e for e in engines if e in allowed]

    best: Result | None = None
    for name in engines:
        res = get_instance(name)(payload)
        if res.candidates:
            if best is None or res.candidates[0].confidence > best.candidates[0].confidence:
                best = res
                if res.candidates[0].confidence >= 0.99:
                    break
    if (best is None or best.candidates[0].confidence == 0.0) and cap_bytes is not None and isinstance(source, (str, Path)):
        payload = Path(source).read_bytes()
        for name in engines:
            res = get_instance(name)(payload)
            if res.candidates:
                best = res
                break
    if best is None:
        best = Result(
            candidates=[Candidate(media_type="application/octet-stream", confidence=0.0)]
        )
    if cache and isinstance(source, (str, Path)):
        cache_put(Path(source), best)
    return best
try:
    import anyio as _anyio
    async def detect_async(source: Any, **kw) -> Result:
        return await _anyio.to_thread.run_sync(detect, source, **kw)
except ImportError:
    pass
def scan_dir(
    root: str | Path,
    *,
    pattern: str = "**/*",
    workers: int = os.cpu_count() or 4,
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
    ignore_set = set(DEFAULT_IGNORES)
    if ignore:
        ignore_set.update(Path(d).name for d in ignore)
    paths = []
    for p in root.glob(pattern):
        if not p.is_file():
            continue
        if ignore_set and any(part in ignore_set for part in p.relative_to(root).parts):
            continue
        paths.append(p)
    if extensions is not None:
        allowed = {e.lower().lstrip('.') for e in extensions}
        paths = [p for p in paths if p.suffix.lower().lstrip('.') in allowed]
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(detect, p, only=only, extensions=extensions, **kw): p
            for p in paths
        }

        for fut in cf.as_completed(futs):
            yield futs[fut], fut.result()
