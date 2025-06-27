from __future__ import annotations
import ast
import logging
from importlib import import_module
from pathlib import Path

logger = logging.getLogger(__name__)

_pkg_dir = Path(__file__).resolve().parent
_BUILTINS: dict[str, str] = {}
_scanned = False


def _ensure_scanned() -> None:
    global _scanned
    if _scanned:
        return
    for _file in _pkg_dir.glob("*.py"):
        if _file.stem == "__init__":
            continue
        try:
            tree = ast.parse(_file.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - best effort logging
            logger.debug("parse failed for %s", _file, exc_info=exc)
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign):
                        for tgt in stmt.targets:
                            if isinstance(tgt, ast.Name) and tgt.id == "name":
                                if isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                                    _BUILTINS[stmt.value.value] = f"{__name__}.{_file.stem}"
                                break
    _scanned = True


def load_engine(name: str) -> None:
    """Import the module providing ``name`` if it exists."""
    _ensure_scanned()
    mod = _BUILTINS.get(name)
    if mod:
        import_module(mod)


def load_all() -> None:
    """Import all builtin engines."""
    _ensure_scanned()
    for name in list(_BUILTINS):
        load_engine(name)


__all__: list[str] = []
