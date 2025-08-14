from http.server import BaseHTTPRequestHandler, HTTPServer

from key_value_store import KeyValueStore


class KeyValueStoreHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the key-value store API.
    """

    def __init__(self, *args, store=None, **kwargs):
        self.store = store or KeyValueStore()
        super().__init__(*args, **kwargs)


    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass


def run(server_class=HTTPServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, KeyValueStoreHandler)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()