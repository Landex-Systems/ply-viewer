#!/usr/bin/env python3
"""Serve this folder on http://localhost:8000 so the viewer can fetch scenes/ (browsers block fetch() from file://).
Files are served with Content-Length and Range support, so big point clouds show a progress bar."""
import http.server, sys
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache'); super().end_headers()
    def log_message(self, fmt, *a): pass
print(f'PLY viewer at http://localhost:{port}/  (Ctrl-C to stop)')
http.server.ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
