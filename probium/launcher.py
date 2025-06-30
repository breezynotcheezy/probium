"""Launch the Probium backend alongside the Next.js UI."""
from __future__ import annotations

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

import uvicorn

from backend.main import app


def _start_backend() -> subprocess.Popen[bytes]:
    """Start the FastAPI backend in a background process."""
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def _start_frontend() -> subprocess.Popen[bytes]:
    """Start the Next.js development server."""
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env.setdefault("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    return subprocess.Popen(
        ["pnpm", "dev"],
        cwd=str(root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def main() -> None:
    backend_proc = _start_backend()
    # Give the backend a moment to start
    time.sleep(1)
    frontend_proc = _start_frontend()
    webbrowser.open("http://127.0.0.1:3000")

    try:
        frontend_proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        frontend_proc.terminate()
        backend_proc.terminate()
        frontend_proc.wait()
        backend_proc.wait()


if __name__ == "__main__":
    main()
