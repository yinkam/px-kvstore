from http.server import BaseHTTPRequestHandler, HTTPServer


def run(server_class=HTTPServer, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, BaseHTTPRequestHandler)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()