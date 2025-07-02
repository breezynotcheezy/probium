from importlib.metadata import entry_points, version
from typing import TYPE_CHECKING
from .core import detect, scan_dir, list_engines
from .google_magika import detect_magika
from .magic_service import detect_magic
from .trid_multi import detect_with_trid
from .exceptions import EngineFailure, FastbackError, UnsupportedType
from .registry import register

def watch(*args, **kw):
    """Lazily import and invoke :func:`probium.watch.watch`."""
    from .watch import watch as _watch
    return _watch(*args, **kw)
__all__ = [
    "detect",
    "scan_dir",
    "list_engines",
    "register",
    "FastbackError",
    "UnsupportedType",
    "EngineFailure",
    "detect_with_trid",
    "detect_magic",
    "detect_magika",
    "watch",

]
try:
    from .core import detect_async
except ImportError:
    if TYPE_CHECKING:
        from typing import Any, Coroutine
        async def detect_async(*args: Any, **kw: Any) -> "Coroutine[Any, Any, None]": ...
    else:
        async def detect_async(*_a, **_kw):
            raise RuntimeError("Install 'anyio' to use detect_async()")
    __all__.append("detect_async")
else:
    __all__.append("detect_async")
try:
    from importlib.metadata import version
    __version__ = version("probium")
except Exception:
    __version__ = "0.0.0-dev"

for ep in entry_points(group="probium.engines"):
    ep.load()
