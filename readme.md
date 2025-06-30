# Probium 🌑

Probium is a fast, modular content analysis tool that detects and classifies file types using pluggable detection engines. Built for high-throughput environments, it supports both API and CLI usage.

## Features

- Fast file type detection ✔
- Pluggable engine architecture (PDF, ZIP, etc.) ✔
- Python library and CLI interface ✔
- Parallel scanning with thread pools ✔
- JSON output for easy integration ✔

### Usage:
"*pip install probium*"


## ☑️ CLI ☑️

### To scan a file or folder
"probium detect path/to/file_or_folder"


### To monitor a folder for new files
"probium watch path/to/folder"



## ☑️ Python Library ☑️


### 1) Import

from probium import detect, detect_magic, scan_dir


### 2) Peek at one file
meta = detect("sample.pdf")            # returns a rich Pydantic model
print("SHA-256 🔮", meta.hash.sha256)  # 🍇 easy attribute access

meta_fast = detect_magic(b"%PDF-1.4\n...")  # use magic-number lookup

### 3) Fine-tune if you like
meta = detect(
    "sample.pdf",
    only=["hash", "pdf"],   # run just these engines
    cap_bytes=1_000_000     # read at most 1 MB
)

### 4) Stream-scan an entire folder
for path, m in scan_dir("docs", pattern="**/*.pdf", workers=4):
    print(f"{path} → {m.mimetype} · {m.size:,} bytes 🍇")

### 5) Monitor a folder for new files
def handle(path, result):
    print(path, "→", result.candidates[0].media_type)

wc = watch("incoming", handle, extensions=["pdf", "docx"])

wc.stop()

## 🖥️ UI Launcher 🖥️

Install the Node dependencies once:

```
pnpm install
```

Then start the full stack development environment with:

```
probium-ui
```

This command runs the FastAPI backend and the Next.js UI together. Your browser will open at `http://localhost:3000` with the UI connected to the API on port 8000.
