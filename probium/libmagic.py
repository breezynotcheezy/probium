from __future__ import annotations
import logging

logger = logging.getLogger(__name__)


def load_magic():
    """Return a libmagic detector or ``None`` if unavailable."""
    try:
        import magic  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dep missing
        logger.warning("python-magic not installed: %s", exc)
        return None
    try:
        return magic.Magic(mime=True)
    except Exception as exc:  # pragma: no cover - runtime failure
        logger.warning("libmagic unavailable: %s", exc)
        return None
