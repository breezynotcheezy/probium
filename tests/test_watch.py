import time
from pathlib import Path
from probium.watch import watch


def test_watch(tmp_path):
    events: list[tuple[Path, str]] = []

    def cb(path: Path, res):
        events.append((path, res.candidates[0].media_type))

    wc = watch(tmp_path, cb, recursive=False)
    try:
        f = tmp_path / "sample.txt"
        f.write_bytes(b"hello world")
        for _ in range(20):
            if events:
                break
            time.sleep(0.1)
        assert events and events[0][0] == f
        assert events[0][1]
    finally:
        wc.stop()
