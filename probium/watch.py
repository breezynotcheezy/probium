"""File system watchers that run detection on new files."""
from __future__ import annotations
from pathlib import Path
from typing import Callable, Iterable, Any
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from .core import _detect_file as detect
from .models import Result

logger = logging.getLogger(__name__)


class _FilterHandler(FileSystemEventHandler):
    def __init__(
        self,
        callback: Callable[[Path, Result], Any],
        *,
        only: Iterable[str] | None = None,
        extensions: Iterable[str] | None = None,
    ) -> None:
        self.callback = callback
        self.only = set(only) if only else None
        self.extensions = (
            {e.lower().lstrip(".") for e in extensions} if extensions else None
        )

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events only.

        ``watchdog`` typically emits a ``created`` event followed by a
        ``modified`` event for the same file.  Calling the detection logic for
        both events results in duplicate scans, so we only trigger on creation
        to ensure each file is processed once.
        """
        self._handle(event)

    def _handle(self, event: FileSystemEvent) -> None:
        path = Path(event.src_path)
        if path.is_dir():
            return
        if self.extensions and path.suffix.lower().lstrip(".") not in self.extensions:
            return
        res = detect(path, only=self.only, extensions=self.extensions, cap_bytes=None)
        try:
            self.callback(path, res)
        except Exception:
            logger.exception("watcher callback failed for %s", path)


class WatchContainer:
    """Simple wrapper around :mod:`watchdog` observers."""

    def __init__(
        self,
        root: str | Path,
        callback: Callable[[Path, Result], Any],
        *,
        recursive: bool = True,
        only: Iterable[str] | None = None,
        extensions: Iterable[str] | None = None,
    ) -> None:
        self.root = Path(root)
        self.callback = callback
        self.recursive = recursive
        self.handler = _FilterHandler(callback, only=only, extensions=extensions)
        self.observer = Observer()

    def start(self) -> None:
        """Begin monitoring ``root`` for filesystem events."""

        self.observer.schedule(self.handler, str(self.root), recursive=self.recursive)
        self.observer.start()

    def stop(self) -> None:
        """Stop the observer and wait for the thread to exit."""

        self.observer.stop()
        self.observer.join()


def watch(
    root: str | Path,
    callback: Callable[[Path, Result], Any],
    *,
    recursive: bool = True,
    only: Iterable[str] | None = None,
    extensions: Iterable[str] | None = None,
) -> WatchContainer:
    """Start watching ``root`` and invoke ``callback`` for new files."""
    container = WatchContainer(
        root, callback, recursive=recursive, only=only, extensions=extensions
    )
    container.start()
    return container
