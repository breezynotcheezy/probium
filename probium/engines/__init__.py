# Register your own engine into 'probium/engines/' and it will auto-register here.
from importlib import import_module
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

_pkg_dir = Path(__file__).resolve().parent
for _file in _pkg_dir.glob("*.py"):
    if _file.stem != "__init__":
        try:
            import_module(f"{__name__}.{_file.stem}")
        except Exception as exc:  # pragma: no cover - best effort logging
            logger.debug("Engine %s failed to load", _file.stem, exc_info=exc)
