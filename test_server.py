import unittest
import threading
import time
import json
import urllib.request
from urllib.error import HTTPError

import server


class TestKVServer(unittest.TestCase):
    PORT = 8000
    SERVER_URL = f"http://localhost:{PORT}"

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=server.run, daemon=True)
        cls.server_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # A test-specific key to ensure each test is independent
        self.key = f"testkey-{self.id()}"

    def _make_request(self, method, endpoint, data=None):
        url = self.SERVER_URL + endpoint
        request_data = None
        headers = {}
        if data:
            request_data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'

        req = urllib.request.Request(url, data=request_data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read()
                return response, content
        except urllib.error.HTTPError as e:
            content = e.read()
            return e, content

    def test_create_and_read(self):
        """
        Test that a new key can be created and read.
        """

        # Create a new key
        data = {'key': self.key, 'value': 'somevalue'}
        response, content = self._make_request('POST', '/', data=data)
        self.assertEqual(response.status, 201)

        # Read the key we just created
        response, content = self._make_request('GET', f'/?key={self.key}')
        self.assertEqual(response.status, 200)

        response_body = json.loads(content)
        self.assertEqual(response_body['value'], 'somevalue')

    def test_update_existing_key(self):
        # First, create a key to update
        data = {'key': self.key, 'value': 'originalvalue'}
        self._make_request('POST', '/', data=data)

        # Now update it
        data = {'key': self.key, 'value': 'updatedvalue'}
        response, content = self._make_request('POST', '/', data=data)
        self.assertEqual(response.status, 201)

        # Verify the update by reading the key again
        response, content = self._make_request('GET', f'/?key={self.key}')
        self.assertEqual(response.status, 200)
        response_body = json.loads(content)
        self.assertEqual(response_body['value'], 'updatedvalue')

    def test_delete_key(self):
        # First, create a key to delete
        data = {'key': self.key, 'value': 'todelete'}
        self._make_request('POST', '/', data=data)

        # Now delete it
        response, content = self._make_request('DELETE', f'/?key={self.key}')
        self.assertEqual(response.status, 200)

        # Verify deletion
        response, content = self._make_request('GET', f'/?key={self.key}')
        self.assertEqual(response.status, 404)

    def test_key_not_found_on_read(self):
        response, content = self._make_request('GET', f'/?key={self.key}')
        self.assertEqual(response.status, 404)

    def test_key_not_found_on_delete(self):
        response, content = self._make_request('DELETE', f'/?key={self.key}')
        self.assertEqual(response.status, 404)


if __name__ == '__main__':
    unittest.main()