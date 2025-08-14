import threading
from typing import Any, Optional

store = {}
lock = threading.Lock()


class KeyValueStore:
    """
    Thread-safe in-memory key-value store implementation.
    """

    def create_or_update(self, key: str, value: Any) -> bool:
        """
        Create or Update a new key-value pair.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        with lock:
            store[key] = value
            return True

    def read(self, key: str) -> Optional[Any]:
        """
        Read a value by key.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        with lock:
            return store.get(key)

    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        with lock:
            if key not in store:
                return False
            del store[key]
            return True