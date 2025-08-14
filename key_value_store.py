import threading
from typing import Any, Dict, Optional


class KeyValueStore:
    """
    Thread-safe in-memory key-value store implementation.
    """

    def __init__(self):
        self._db: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def create(self, key: str, value: Any) -> bool:
        """
        Create a new key-value pair.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        with self._lock:
            if key in self._db:
                return False
            self._db[key] = value
            return True

    def read(self, key: str) -> Optional[Any]:
        """
        Read a value by key.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        with self._lock:
            return self._db.get(key)

    def update(self, key: str, value: Any) -> bool:
        """
        Update an existing key-value pair.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        with self._lock:
            if key not in self._db:
                return False
            self._db[key] = value
            return True

    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        with self._lock:
            if key not in self._db:
                return False
            del self._db[key]
            return True