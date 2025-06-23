import concurrent.futures
from probium import detect
from .test_engines import BASE_SAMPLES


def test_engine_cache_thread_safe():
    payload = BASE_SAMPLES["python"]

    def run():
        for _ in range(20):
            res = detect(payload, engine="python", cap_bytes=None)
            assert res.candidates

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(run) for _ in range(8)]
        for f in concurrent.futures.as_completed(futs):
            f.result()
