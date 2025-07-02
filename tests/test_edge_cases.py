from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from probium import detect
from probium.watch import watch

SAMPLES_DIR = Path(__file__).parent / "samples"


def test_detect_negative_capbytes():
    path = SAMPLES_DIR / "sample.csv"
    res = detect(path, cap_bytes=-10)
    cand = res.candidates[0]
    assert cand.media_type == "text/csv"
    assert cand.extension == "csv"


def test_watch_missing_root(tmp_path):
    missing = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        watch(missing, lambda p, r: None)
