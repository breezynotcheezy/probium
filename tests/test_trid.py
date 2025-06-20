from probium import detect_with_trid
from .test_engines import BASE_SAMPLES


def test_detect_with_trid_returns_mapping():
    res = detect_with_trid(BASE_SAMPLES["png"], cap_bytes=None)
    assert "probium" in res and "trid" in res
    assert res["probium"].candidates
