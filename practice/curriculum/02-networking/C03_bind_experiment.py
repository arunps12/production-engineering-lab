"""
Exercise 2.C.3 — 0.0.0.0 vs 127.0.0.1 Experiment
Guide: docs/curriculum/02-networking-debug-lab.md

Tasks:
1. Start a server on 127.0.0.1 — only accessible locally
2. Start a server on 0.0.0.0 — accessible from other machines
3. Verify with curl from localhost and another machine
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler


def start_server(host, port=8080):
    """Start an HTTP server on the given host:port."""
    # TODO: Create and start the server
    # server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    # print(f"Serving on {host}:{port}")
    # server.serve_forever()
    pass


# TODO: Try with 127.0.0.1 then 0.0.0.0
# start_server("127.0.0.1", 8080)
# start_server("0.0.0.0", 8080)
