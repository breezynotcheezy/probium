# Probium

Probium is a fast, modular content analysis tool that detects and classifies file types using pluggable detection engines. Built for high-throughput environments, it supports both API and CLI usage.

## Features

- ⚡ Blazing-fast file type detection
- 🧩 Pluggable engine architecture (PDF, ZIP, etc.)
- 📦 Python library and CLI interface
- 🔁 Parallel scanning with thread pools
- 🧠 JSON output for easy integration

## Installation

```bash
pip install probium

Usage:

* CLI
To scan a single file
python -m probium one path/to/file

To recursively scan a folder
python -m probium all path/to/folder

Probium skips `.git`, `venv`, `.venv` and `__pycache__` by default. You can
specify additional directories with `--ignore`:

```bash
python -m probium all path/to/folder --ignore node_modules build
```


* Python Library
from probium import detect

result = detect("path/to/file")
print(result.model_dump_json())


# Clone and install locally
git clone https://github.com/your-org/probium.git
cd probium
pip install -e .

## Testing

Install dependencies and run the engine test harness with:

```bash
pip install -e .
pytest
```
