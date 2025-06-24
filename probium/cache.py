# probium/cache.py  – thread-safe SQLite + small in-mem LRU
from __future__ import annotations
import sqlite3
import time
from pathlib import Path
from typing import Optional

from platformdirs import user_cache_dir
from cachetools import LRUCache
from threading import RLock

from .models import Result


CACHE_DIR = Path(user_cache_dir("probium"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DB = CACHE_DIR / "results.sqlite3"

_DB_TIMEOUT = 30.0


def _init_db() -> None:
    """Create the cache database if needed."""
    with sqlite3.connect(DB, timeout=_DB_TIMEOUT) as con:
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("CREATE TABLE IF NOT EXISTS r (p TEXT PRIMARY KEY, t REAL, j TEXT)")
        con.commit()


def _reset_db() -> None:
    """Remove a corrupted cache database and recreate it."""
    try:
        DB.unlink()
    except FileNotFoundError:
        pass

    except PermissionError:
        # another process may still have the file open
        return

    _init_db()


_init_db()

_mem: LRUCache[str, str] = LRUCache(maxsize=1024)
_mem_lock = RLock()
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
    with _mem_lock:
        if key in _mem:
            return _des(_mem[key])


    # L2: SQLite (own connection per thread)
    try:

        with sqlite3.connect(DB, timeout=_DB_TIMEOUT) as con:
            row = con.execute("SELECT t, j FROM r WHERE p = ?", (key,)).fetchone()
            if not row:
                return None
            ts, raw = row
            if _now() - ts > TTL:
                return None
    except sqlite3.DatabaseError:
        _reset_db()
        return None

    with _mem_lock:
        _mem[key] = raw
    return _des(raw)


def put(path: Path, result: Result) -> None:
    key = str(path.resolve())
    raw = _ser(result)
    with _mem_lock:
        _mem[key] = raw
    try:
        with sqlite3.connect(DB, timeout=_DB_TIMEOUT) as con:
            con.execute(
                "INSERT OR REPLACE INTO r (p, t, j) VALUES (?,?,?)",
                (key, _now(), raw),
            )
            con.commit()
    except sqlite3.DatabaseError:
        _reset_db()
