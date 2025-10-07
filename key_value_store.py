import threading
from typing import Any, Optional

store = {}
lock = threading.Lock()

operation_log = []


class KeyValueStore:
    """
    Thread-safe in-memory key-value store implementation.
    """

    def create(self, key: str, value: Any) -> bool:
        """
        Create or Update a new key-value pair.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        
        operation_log.append({"operation": "POST", "key": key, "value": value, "last_value": None})
        
        with lock:
            store[key] = value
            return True
        
    def update(self, key: str, value: Any) -> bool:
        """
        Update a new key-value pair.
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        
        last_value= store[key] 
        operation_log.append({"operation": "PUT", "key": key, "value": value, "last_value": last_value})
        
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
            operation_log.append({"operation": "DELETE", "key": key, "value": store[key], "last_value": None})
            del store[key]
            return True
        
    def undo(self):
        last_operation = operation_log.pop()
        operation = last_operation["operation"]
        key = last_operation["key"]
        value = last_operation["value"]
        last_value = last_operation["last_value"]
        
        
        if operation == "POST":
            del store[key]
        elif operation == "DELETE":
            store[key] = value
        elif operation == "PUT":
            store[key] = last_value
            
        