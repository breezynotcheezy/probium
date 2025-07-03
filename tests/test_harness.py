from pathlib import Path
import sys, os
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import time
import asyncio
import pytest

from probium import detect, detect_async, detect_magika, scan_dir

# Directory containing sample files for tests
SAMPLES_DIR = Path(__file__).parent / "samples"

# Expected results for the sample files
TEST_CASES = {
    "sample.csv": {
        "media_type": "text/csv",
        "extension": "csv",
    },
    "weird.json": {
        "media_type": "application/json",
        "extension": "json",
    },
    "json_prefixed.txt": {
        "media_type": "application/json",
        "extension": "json",
    },
    "json_spoofed_pdf.txt": {
        "media_type": "application/json",
        "extension": "json",
    },
    "empty.txt": {
        "media_type": "*UNSAFE* / *NO ENGINE*",
        "extension": None,
    },
}

LOG_FILE = Path(__file__).parent / "results.json"

@pytest.fixture(scope="session")
def results_log():
    logs = []
    yield logs
    with LOG_FILE.open("w", encoding="utf-8") as fh:
        json.dump(logs, fh, indent=2)

@pytest.mark.parametrize("file_name,expect", list(TEST_CASES.items()))
def test_detect_sync(file_name: str, expect: dict, results_log: list):
    """Validate sync detection for each sample file."""
    path = SAMPLES_DIR / file_name
    start = time.perf_counter()
    try:
        res = detect(path, cap_bytes=None)
    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        results_log.append({
            "file": file_name,
            "passed": False,
            "error": str(exc),
            "elapsed_ms": elapsed,
        })
        raise
    elapsed = (time.perf_counter() - start) * 1000
    cand = res.candidates[0] if res.candidates else None

    passed = (
        cand is not None
        and cand.media_type == expect["media_type"]
        and cand.extension == expect["extension"]
    )

    results_log.append({
        "file": file_name,
        "passed": passed,
        "media_type": cand.media_type if cand else None,
        "extension": cand.extension if cand else None,
        "confidence": cand.confidence if cand else None,
        "elapsed_ms": elapsed,
    })

    assert cand is not None, "No candidate returned"
    assert cand.media_type == expect["media_type"]
    assert cand.extension == expect["extension"]

@pytest.mark.parametrize("file_name,expect", list(TEST_CASES.items()))
def test_detect_async(file_name: str, expect: dict, results_log: list):
    """Validate async detection mirrors sync detection."""
    path = SAMPLES_DIR / file_name
    start = time.perf_counter()
    try:
        res = asyncio.run(detect_async(path, cap_bytes=None))
    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        results_log.append({
            "file": f"async:{file_name}",
            "passed": False,
            "error": str(exc),
            "elapsed_ms": elapsed,
        })
        raise
    elapsed = (time.perf_counter() - start) * 1000
    cand = res.candidates[0] if res.candidates else None
    passed = (
        cand is not None
        and cand.media_type == expect["media_type"]
        and cand.extension == expect["extension"]
    )
    results_log.append({
        "file": f"async:{file_name}",
        "passed": passed,
        "media_type": cand.media_type if cand else None,
        "extension": cand.extension if cand else None,
        "confidence": cand.confidence if cand else None,
        "elapsed_ms": elapsed,
    })
    assert cand is not None, "No candidate returned (async)"
    assert cand.media_type == expect["media_type"]
    assert cand.extension == expect["extension"]


def test_watch_polling(monkeypatch, tmp_path):
    """watch() should fall back to polling when watchdog is unavailable."""
    import probium.watch as w

    monkeypatch.setattr(w, "USING_STUB", True)

    paths: list[Path] = []
    wc = w.watch(tmp_path, lambda p, r: paths.append(p), interval=0.1)
    try:
        f = tmp_path / "foo.txt"
        f.write_text("hi")
        deadline = time.time() + 2
        while not paths and time.time() < deadline:
            time.sleep(0.05)
    finally:
        wc.stop()

    assert paths and paths[0] == f


def test_detect_magika():

    pytest.importorskip("magika")

    path = SAMPLES_DIR / "sample.csv"
    res = detect_magika(path)
    cand = res.candidates[0]
    assert cand.media_type == "text/csv"
    assert cand.extension == "csv"


def test_scan_dir_processes():
    results = list(scan_dir(SAMPLES_DIR, processes=2, workers=1))
    assert results
