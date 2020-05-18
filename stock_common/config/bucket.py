import threading
from typing import Optional


class ConfigBucket:
    def __init__(self):
        self._data = {}
        self._data_version = {}
        self._lock = threading.Lock()

    def get_int(self, key: str) -> Optional[int]:
        """Get the value for a given key as an integer.

        :param key: Key for the value to be returned.
        :return: Integer that maps to the given key.
        """

        val = self._data.get(key)
        if not val:
            return None
        return int(val)

    def get_str(self, key: str) -> Optional[str]:
        """Get the value for a given key as a string.

        :param key: Key for the value to be returned.
        :return: String that maps to the given key.
        """

        val = self._data.get(key)
        if not val:
            return None
        return str(val)

    def remove(self, key: str) -> None:
        """Remove the value for a given key.

        :param key: Key for the value to be removed.
        """

        self._lock.acquire()
        try:
            if key not in self._data:
                return

            del self._data[key]
            del self._data_version[key]
        finally:
            self._lock.release()

    def update(self, key: str, val: str, version: int) -> bool:
        """Update the value for the given key, if the version is greater than the current version.

        :param key: Key for the data to be updated.
        :param val: Value associated with the given key.
        :param version: Version associated with the given value.
        :return: Whether or not the data has been updated.
        """

        self._lock.acquire()
        try:
            if key in self._data_version and version <= self._data_version[key]:
                return False

            self._data[key] = val
            self._data_version[key] = version
        finally:
            self._lock.release()
        return True
