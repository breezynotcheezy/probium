"""Very small polling-based fallback for :mod:`watchdog`."""

from __future__ import annotations

from pathlib import Path
from threading import Event, Thread
import time

from ..events import FileSystemEvent


class Observer:
    """Naïve observer that polls for new files."""

    def __init__(self) -> None:
        self._watches: list[tuple[Path, object, bool]] = []
        self._threads: list[Thread] = []
        self._stop = Event()

    def schedule(self, handler, path: str | Path, recursive: bool = True) -> None:
        self._watches.append((Path(path), handler, recursive))

    def start(self) -> None:
        for root, handler, recursive in self._watches:
            t = Thread(target=self._loop, args=(root, handler, recursive), daemon=True)
            t.start()
            self._threads.append(t)

    def _loop(self, root: Path, handler, recursive: bool) -> None:
        seen: set[Path] = set()
        while not self._stop.is_set():
            globber = root.rglob("*") if recursive else root.glob("*")
            for p in globber:
                if p.is_file() and p not in seen:
                    seen.add(p)
                    event = FileSystemEvent(str(p))
                    if hasattr(handler, "on_created"):
                        handler.on_created(event)
            time.sleep(1.0)

    def stop(self) -> None:
        self._stop.set()

    def join(self, *a, **kw) -> None:
        for t in self._threads:
            t.join(*a, **kw)
