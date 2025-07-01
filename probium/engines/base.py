from __future__ import annotations
import abc, time, logging, hashlib, threading
from cachetools import LRUCache
from ..models import Result
from ..exceptions import EngineFailure

logger = logging.getLogger(__name__)
class EngineBase(abc.ABC):
    name: str = "abstract"
    cost: float = 1.0
    cache_size: int = 256

    def __init__(self) -> None:
        self._cache: LRUCache[str, Result] = LRUCache(maxsize=self.cache_size)
        self._lock = threading.RLock()

    def __call__(self, payload: bytes) -> Result:
        """Run :meth:`sniff` with caching and timing instrumentation."""

        t0 = time.perf_counter()
        digest = hashlib.md5(payload).hexdigest()
        with self._lock:
            cached = self._cache.get(digest)
        if cached is not None:
            cached = cached.model_copy(deep=True)
            cached.engine = self.name
            cached.elapsed_ms = (time.perf_counter() - t0) * 1000
            cached.bytes_analyzed = len(payload)
            cached.hash = digest
            return cached
        try:
            res = self.sniff(payload)
        except Exception as exc:
            logger.exception("%s failed", self.name)
            raise EngineFailure(str(exc)) from exc
        res.engine = self.name
        res.elapsed_ms = (time.perf_counter() - t0) * 1000
        res.bytes_analyzed = len(payload)
        res.hash = digest
        with self._lock:
            self._cache[digest] = res
        return res
    @abc.abstractmethod
    def sniff(self, payload: bytes) -> Result:
        """Examine ``payload`` and return a :class:`~probium.models.Result`."""

        ...
