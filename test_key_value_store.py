#!/usr/bin/env python3
"""
Unit tests for the Key-Value Store implementation.
"""

import unittest
from key_value_store import KeyValueStore


class TestKeyValueStore(unittest.TestCase):
    """Test cases for the KeyValueStore class."""
    
    def setUp(self):
        """Set up a fresh store instance before each test."""
        self.store = KeyValueStore()
    
    def test_create_success(self):
        """Test successful creation of a key-value pair."""
        result = self.store.create("test_key", "test_value")
        self.assertTrue(result)
        self.assertEqual(self.store.read("test_key"), "test_value")
    
    def test_create_duplicate_key(self):
        """Test that creating a duplicate key returns False."""
        self.store.create("test_key", "test_value")
        result = self.store.create("test_key", "another_value")
        self.assertFalse(result)
        self.assertEqual(self.store.read("test_key"), "test_value")
    
    def test_create_invalid_key_type(self):
        """Test that creating with non-string key raises ValueError."""
        with self.assertRaises(ValueError):
            self.store.create(123, "test_value")
    
    def test_read_existing_key(self):
        """Test reading an existing key."""
        self.store.create("test_key", "test_value")
        value = self.store.read("test_key")
        self.assertEqual(value, "test_value")
    
    def test_read_nonexistent_key(self):
        """Test reading a non-existent key returns None."""
        value = self.store.read("nonexistent_key")
        self.assertIsNone(value)
    
    def test_read_invalid_key_type(self):
        """Test that reading with non-string key raises ValueError."""
        with self.assertRaises(ValueError):
            self.store.read(123)
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        self.store.create("test_key", "old_value")
        result = self.store.update("test_key", "new_value")
        self.assertTrue(result)
        self.assertEqual(self.store.read("test_key"), "new_value")
    
    def test_update_nonexistent_key(self):
        """Test that updating a non-existent key returns False."""
        result = self.store.update("nonexistent_key", "new_value")
        self.assertFalse(result)
    
    def test_update_invalid_key_type(self):
        """Test that updating with non-string key raises ValueError."""
        with self.assertRaises(ValueError):
            self.store.update(123, "new_value")
    
    def test_delete_existing_key(self):
        """Test deleting an existing key."""
        self.store.create("test_key", "test_value")
        result = self.store.delete("test_key")
        self.assertTrue(result)
        self.assertIsNone(self.store.read("test_key"))
    
    def test_delete_nonexistent_key(self):
        """Test that deleting a non-existent key returns False."""
        result = self.store.delete("nonexistent_key")
        self.assertFalse(result)
    
    def test_delete_invalid_key_type(self):
        """Test that deleting with non-string key raises ValueError."""
        with self.assertRaises(ValueError):
            self.store.delete(123)

    
    def test_crud_operations_sequence(self):
        """Test a sequence of CRUD operations."""
        # Create
        self.assertTrue(self.store.create("user:1", {"name": "John", "age": 30}))
        
        # Read
        user = self.store.read("user:1")
        self.assertEqual(user["name"], "John")
        self.assertEqual(user["age"], 30)
        
        # Update
        self.assertTrue(self.store.update("user:1", {"name": "John", "age": 31}))
        updated_user = self.store.read("user:1")
        self.assertEqual(updated_user["age"], 31)
        
        # Delete
        self.assertTrue(self.store.delete("user:1"))
        self.assertIsNone(self.store.read("user:1"))


if __name__ == "__main__":
    unittest.main(verbosity=2) 