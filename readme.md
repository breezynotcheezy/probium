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

### To scan a single file
"probium one path/to/file"



### To recursively scan a folder
"probium all path/to/folder"



## ☑️ Python Library ☑️


### 🟣 1) import the magic
from probium import detect, scan_dir

### 🟪 2) Peek at one file
meta = detect("sample.pdf")            # returns a rich Pydantic model
print("SHA-256 🔮", meta.hash.sha256)  # 🍇 easy attribute access

### 🟣 3) Fine-tune if you like
meta = detect(
    "sample.pdf",
    only=["hash", "pdf"],   # run just these engines
    cap_bytes=1_000_000     # read at most 1 MB
)

### 💜 4) Stream-scan an entire folder
for path, m in scan_dir("docs", pattern="**/*.pdf", workers=4):
    print(f"{path} → {m.mimetype} · {m.size:,} bytes 🍇")


