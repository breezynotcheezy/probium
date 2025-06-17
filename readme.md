# Probium

## Probium (formerly fastbackfilter) is a high-performance, pluggable content detection engine designed for use in compliance, digital forensics, and large-scale file analysis workflows. It scans files or directories and returns structured JSON output indicating detected file types with confidence scores.


### Features

Multithreaded directory scanning

Pluggable engine architecture (e.g., PDF, ZIP, fallback detectors)

Heuristic and magic-byte based detection

Structured, typed JSON output

Optional SQLite-based caching for repeated scans

Minimal CLI with support for batch or single-file scans

Installation
Install the latest version from PyPI:

bash
Copy
Edit
pip install probium
For local development:

bash
Copy
Edit
git clone https://github.com/your-org/probium.git
cd probium
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
Usage
Scan a single file
bash
Copy
Edit
python -m fastbackfilter.cli one path/to/file.ext
Scan all files in a directory recursively
bash
Copy
Edit
python -m fastbackfilter.cli all path/to/root
Optional flags:

--raw: Outputs compact (minified) JSON

--pattern: Glob pattern to include (default: **/*)

--workers: Number of threads (default: 4)

Sample Output
json
Copy
Edit
{
  "path": "sample.pdf",
  "engine": "pdf",
  "bytes_analyzed": 76292,
  "elapsed_ms": 0.68,
  "candidates": [
    {
      "media_type": "application/pdf",
      "extension": "pdf",
      "confidence": 1.0,
      "breakdown": {
        "offset": 0.0
      }
    }
  ],
  "error": null
}

