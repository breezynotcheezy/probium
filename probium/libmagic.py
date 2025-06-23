from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

_SENTINEL = object()
_cached_magic: object | None = _SENTINEL


def load_magic():
    """Return a cached libmagic detector or ``None`` if unavailable."""
    global _cached_magic
    if _cached_magic is not _SENTINEL:
        return _cached_magic  # type: ignore[return-value]
    try:
        import magic  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dep missing
        logger.debug("python-magic not installed", exc_info=exc)
        _cached_magic = None
        return None
    try:
        _cached_magic = magic.Magic(mime=True)
    except Exception as exc:  # pragma: no cover - runtime failure
        logger.debug("libmagic unavailable", exc_info=exc)
        _cached_magic = None
    return _cached_magic  # type: ignore[return-value]
