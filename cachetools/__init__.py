from collections import OrderedDict

class LRUCache:
    """Minimal drop-in replacement for cachetools.LRUCache."""
    def __init__(self, maxsize=128):
        self.maxsize = maxsize
        self._data = OrderedDict()

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def get(self, key, default=None):
        if key in self._data:
            value = self._data.pop(key)
            self._data[key] = value
            return value
        return default

    def __getitem__(self, key):
        value = self.get(key)
        if value is None and key not in self._data:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        if key in self._data:
            self._data.pop(key)
        elif len(self._data) >= self.maxsize:
            self._data.popitem(last=False)
        self._data[key] = value

    def pop(self, key, default=None):
        return self._data.pop(key, default)
