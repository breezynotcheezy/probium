# Probium 🌑
<!-- BEGIN LATEST DOWNLOAD BUTTON -->
<!-- END LATEST DOWNLOAD BUTTON -->
Probium is a fast, modular content analysis tool that detects and classifies file types using pluggable detection engines. Built for high-throughput environments, it supports both API and CLI usage.

## Features

- Fast file type detection ✔
- Pluggable engine architecture (PDF, ZIP, etc.) ✔
- Python library and CLI interface ✔
- Parallel scanning with thread pools ✔
- JSON output for easy integration ✔


## Installation

Install Probium and its Python dependencies with ``pip``:

```bash
pip install probium
```

If you are working from a source checkout run ``pip install -e .`` instead.
The optional ``watchdog`` package enables native file system events for the
``probium watch`` command. Without it, a portable polling loop is used which is
slightly slower. To enable native events install ``watchdog`` manually:

```bash
pip install watchdog
```

### Usage:



## ☑️ CLI ☑️

### To scan a file or folder
"probium detect path/to/file_or_folder"

### Use Google Magika instead of built-in engines
"probium detect path/to/file --magika"

*Requires the optional `magika` package*

Probium launches one worker thread per CPU core by default. Override this with
`--workers` if needed.

### Colorize path output by file type
"probium detect path/to/file --color"

### Measure total runtime
"probium detect path/to/file --benchmark"

### Run scanning synchronously
"probium detect path/to/folder --sync"

### Stream results line by line
"probium detect path/to/folder --ndjson"

Probium uses asynchronous scanning by default for maximum performance.



### To monitor a folder for new files
"probium watch path/to/folder"



## ☑️ Python Library ☑️


### 1) Import

from probium import detect, detect_magic, scan_dir

from probium import detect_magika  # requires `magika` package



### 2) Peek at one file
meta = detect("sample.pdf")            # returns a rich Pydantic model
print("SHA-256 🔮", meta.hash.sha256)  # 🍇 easy attribute access

meta_fast = detect_magic(b"%PDF-1.4\n...")  # use magic-number lookup


meta_magika = detect_magika("sample.pdf")  # use Google Magika if installed


### 3) Fine-tune if you like
meta = detect(
    "sample.pdf",
    only=["hash", "pdf"],   # run just these engines
    cap_bytes=1_000_000     # read at most 1 MB
)
# Using a single engine short-circuits the search for near O(1) performance

### 4) Stream-scan an entire folder
for path, m in scan_dir("docs", pattern="**/*.pdf", workers=4):
    print(f"{path} → {m.mimetype} · {m.size:,} bytes 🍇")

### 5) Monitor a folder for new files
def handle(path, result):
    print(path, "→", result.candidates[0].media_type)

wc = watch("incoming", handle, extensions=["pdf", "docx"])

wc.stop()

## 🖥️ UI Launcher 🖥️

Install Node.js (version 18 or newer) and the ``pnpm`` package manager. If
``pnpm`` isn't available, install it with ``npm install -g pnpm``. Then install
the UI dependencies once:


```
pnpm install
```

Then start the UI with:

```
probium-ui
```


This command launches the Next.js interface which internally calls the
``probium`` library via built‑in API routes. ``probium-ui`` tries to run ``pnpm
dev`` and falls back to ``npm run dev`` if ``pnpm`` is missing. Your browser will
open at `http://localhost:3000`.

### Backend API

The frontend communicates with a FastAPI backend that exposes Probium's
functionality. Start the backend with:

```
cd backend && ./start.sh
```

By default the UI expects the backend to be reachable at
`http://localhost:8000`. You can override this by setting the environment
variable `BACKEND_URL` (used by Next.js API routes) or
`NEXT_PUBLIC_API_URL` when launching the UI.

### Authentication

Probium's UI includes a basic login page powered by `next-auth`. Users can
authenticate with an email address, a phone number, or a Google account.
Credentials are hashed using `bcryptjs`. To enable Google login, set the
following environment variables (see `.env.example`):

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
NEXTAUTH_SECRET=your-random-secret
```

