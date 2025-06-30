"""Launch the Next.js UI for Probium."""
from __future__ import annotations

import subprocess
import webbrowser
from pathlib import Path


def _start_frontend() -> subprocess.Popen[bytes]:
    """Start the Next.js development server."""
    root = Path(__file__).resolve().parents[1]
    return subprocess.Popen(
        ["pnpm", "dev"],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


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
