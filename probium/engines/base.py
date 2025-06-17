from __future__ import annotations
import abc, time, logging
from ..types import Result
from ..exceptions import EngineFailure
import hashlib

logger = logging.getLogger(__name__)
class EngineBase(abc.ABC):
    name: str = "abstract"
    cost: float = 1.0
    def __call__(self, payload: bytes) -> Result:
        t0 = time.perf_counter()
        try:
            res = self.sniff(payload)
        except Exception as exc:
            logger.exception("%s failed", self.name)
            raise EngineFailure(str(exc)) from exc
        res.engine = self.name
        res.elapsed_ms = (time.perf_counter() - t0) * 1000
        res.bytes_analyzed = len(payload)

        hash = hashlib.md5()
        #hash = hashlib.sha256()

        hash.update(payload)
        hex_string = hash.hexdigest()
        res.hash = hex_string
        return res
    @abc.abstractmethod
    def sniff(self, payload: bytes) -> Result: ...
