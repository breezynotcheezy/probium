from probium import detect_magic
from .test_engines import BASE_SAMPLES


def test_magic_service_detects_samples():
    for payload in BASE_SAMPLES.values():
        res_magic = detect_magic(payload)
        assert res_magic.candidates
