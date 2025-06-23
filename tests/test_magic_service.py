from probium import detect_magic
from .test_engines import BASE_SAMPLES


def test_magic_service_detects_samples():
    for payload in BASE_SAMPLES.values():
        res_magic = detect_magic(payload)
        assert res_magic.candidates



def test_load_magic_cached():
    import importlib
    from probium import libmagic

    mod = importlib.reload(libmagic)
    first = mod.load_magic()
    second = mod.load_magic()
    assert first is second

