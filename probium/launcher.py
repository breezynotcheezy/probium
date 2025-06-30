"""Launch the Next.js UI for Probium."""
from __future__ import annotations

import subprocess
import webbrowser
from pathlib import Path


def _start_frontend() -> subprocess.Popen[bytes]:
    """Start the Next.js development server.

    We prefer ``pnpm`` but fall back to ``npm`` if ``pnpm`` isn't installed.
    ``FileNotFoundError`` is raised when neither tool exists.
    """
    root = Path(__file__).resolve().parents[1]

    commands = [["pnpm", "dev"], ["npm", "run", "dev"]]
    last_err: Exception | None = None
    for cmd in commands:
        try:
            return subprocess.Popen(
                cmd,
                cwd=str(root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except FileNotFoundError as exc:  # command not found
            last_err = exc

    assert last_err is not None
    raise FileNotFoundError(
        "Neither 'pnpm' nor 'npm' was found. Please install Node.js and pnpm "
        "(https://pnpm.io) before running the UI"
    ) from last_err


def main() -> None:
    frontend_proc = _start_frontend()
    webbrowser.open("http://127.0.0.1:3000")

    try:
        frontend_proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        frontend_proc.terminate()
        frontend_proc.wait()


if __name__ == "__main__":
    main()
