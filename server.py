import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from key_value_store import KeyValueStore


class KeyValueStoreHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the key-value store API.
    """

    def __init__(self, *args, store=None, **kwargs):
        self.store = store or KeyValueStore()
        super().__init__(*args, **kwargs)


    def _set_headers(self, status_code=200):
        """Helper function to set standard HTTP headers."""

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Handles GET requests to read a key."""

        print(self.store)
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        key = query_params.get('key')

        if not key or not key[0]:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Key parameter is required.'}).encode('utf-8'))
            return

        key = key[0]
        value = self.store.read(key)

        if value is not None:
            self._set_headers(200)
            self.wfile.write(json.dumps({'key': key, 'value': value}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': f"Key '{key}' not found."}).encode('utf-8'))

    def do_POST(self):
        """Handles POST requests to create or update a key."""

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        parsed_path = urlparse(self.path)
        
        path_segments = parsed_path.path.lstrip("/").split("/")
        
        if path_segments[-1] == "undo":
            self.store.undo()
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            key = data.get('key')
            value = data.get('value')
            if not key or not value:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Key and value are required.'}).encode('utf-8'))
                return

            self.store.create_or_update(key, value)
            self._set_headers(201)
            self.wfile.write(json.dumps({'message': 'Key created/updated successfully.'}).encode('utf-8'))
        except (json.JSONDecodeError, KeyError):
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Invalid JSON format.'}).encode('utf-8'))

    def do_DELETE(self):
        """Handles DELETE requests to remove a key."""

        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        key = query_params.get('key')

        if not key or not key[0]:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Key parameter is required.'}).encode('utf-8'))
            return

        key = key[0]
        if self.store.delete(key):
            self._set_headers(200)
            self.wfile.write(json.dumps({'message': 'Key deleted successfully.'}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': f"Key '{key}' not found."}).encode('utf-8'))


def run(server_class=HTTPServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, KeyValueStoreHandler)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()