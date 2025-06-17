Probium (formerly FastbackFilter) is a blazing-fast, pluggable content detection engine that recursively scans files, identifies their true types using heuristic and signature-based engines, and outputs structured results in JSON format. Designed for modern compliance, security auditing, and data integrity use cases.

🚀 Features
⚡ Fast, multithreaded scanning of directories or individual files.

🔍 Custom pluggable engines for content detection (e.g., PDFs, archives).

🧠 Heuristic and magic-byte based detection—no reliance on file extensions.

🛠️ CLI + Python API for flexible integration into pipelines and tools.

🪪 Typed JSON output with confidence scores, detection breakdowns, and timing metrics.

💾 Local SQLite cache for repeated scans with expiration control.

📦 Zero fluff. Zero noise. Just results.

📦 Installation
bash
Copy
Edit
pip install probium
To test the latest version locally during development:

bash
Copy
Edit
git clone https://github.com/your-org/probium.git
cd probium
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
🧪 Usage
Scan a single file:
bash
Copy
Edit
python -m fastbackfilter.cli one ./sample.pdf
Recursively scan a directory:
bash
Copy
Edit
python -m fastbackfilter.cli all /path/to/folder
Use --raw to emit compact JSON, and --pattern to control the glob filter.

🧩 Output Example
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
🔧 Architecture
engines/: Modular signature-based detectors (e.g., PDF, ZIP, Fallback).

core.py: Threaded scanning orchestration.

cache.py: SQLite-backed LRU cache with TTL.

cli.py: Lightweight click-based command-line interface.

🔐 Use Cases
🧾 Digital forensics & chain-of-custody verification

🏛️ Government compliance checks (OMB M-23-02, FIPS-validated formats)

🗃️ Archive auditing & media validation

🧬 Data ingestion and pipeline filtering
