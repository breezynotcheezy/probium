from __future__ import annotations
from types import MappingProxyType
from importlib import import_module

from .exceptions import UnsupportedType


_engines: dict[str, type] = {}
_engine_instances: dict[str, "EngineBase"] = {}


def register(cls):
    """Decorator to add an engine class to the global registry."""

    _engines[cls.name] = cls
    return cls


def get(name: str):
    """Return the engine class associated with ``name``."""
    if name not in _engines:
        try:
            import_module(f"probium.engines.{name}")
        except Exception:
            raise UnsupportedType(name)
    try:
        return _engines[name]
    except KeyError as exc:
        raise UnsupportedType(name) from exc

def get_instance(name: str) -> "EngineBase":
    """Return a cached instance of the requested engine."""
    from .engines.base import EngineBase
    cls = get(name)
    if name not in _engine_instances:
        _engine_instances[name] = cls()
    return _engine_instances[name]
def list_engines() -> list[str]:
    """Return engine names ordered by ``cost`` attribute."""
    if not _engines:
        # Import all built-in engines on demand
        import_module("probium.engines").load_all()
    return [
        name
        for name, cls in sorted(
            _engines.items(), key=lambda kv: getattr(kv[1], "cost", 1.0)
        )
        if not getattr(cls, "opt_in_only", False)
    ]
all_engines = lambda: MappingProxyType(_engines)
