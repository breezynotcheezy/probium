# fastbackfilter/cache.py  – thread-safe SQLite + small in-mem LRU
from __future__ import annotations
import sqlite3, time
from pathlib import Path
from typing import Optional

from platformdirs import user_cache_dir
from cachetools import LRUCache

from .types import Result


CACHE_DIR = Path(user_cache_dir("fastbackfilter"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DB = CACHE_DIR / "results.sqlite3"
with sqlite3.connect(DB) as con:
    con.execute(
        "CREATE TABLE IF NOT EXISTS r (p TEXT PRIMARY KEY, t REAL, j TEXT)"
    )
    con.commit()

_mem: LRUCache[str, str] = LRUCache(maxsize=1024)
TTL = 24 * 3600  # 1 day


def _now() -> float:
    return time.time()


def _ser(res: Result) -> str:
    return res.model_dump_json()


def _des(raw: str) -> Result:
    return Result.model_validate_json(raw)


def get(path: Path) -> Optional[Result]:
    key = str(path.resolve())

    # L1: RAM
    if key in _mem:
        return _des(_mem[key])

    # L2: SQLite (own connection per thread)
    with sqlite3.connect(DB) as con:
        row = con.execute(
            "SELECT t, j FROM r WHERE p = ?", (key,)
        ).fetchone()
        if not row:
            return None
        ts, raw = row
        if _now() - ts > TTL:
            return None

    _mem[key] = raw
    return _des(raw)


def put(path: Path, result: Result) -> None:
    key = str(path.resolve())
    raw = _ser(result)
    _mem[key] = raw
    with sqlite3.connect(DB) as con:
        con.execute(
            "INSERT OR REPLACE INTO r (p, t, j) VALUES (?,?,?)",
            (key, _now(), raw),
        )
        con.commit()
