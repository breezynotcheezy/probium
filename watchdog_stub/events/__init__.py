"""Minimal event classes used by the polling fallback."""

class FileSystemEvent:
    def __init__(self, src_path: str, dest_path: str | None = None) -> None:
        self.src_path = src_path
        self.dest_path = dest_path


class FileSystemEventHandler:
    """Base class compatible with :mod:`watchdog`."""
    pass
