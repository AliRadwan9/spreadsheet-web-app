import webbrowser
import http.server
import os
import threading
from urllib.parse import unquote, urlparse

PORT = 8000
CURRENT_DIR = os.path.dirname(__file__)

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        request_path = unquote(parsed.path)

        file_path = None
        if request_path == "/":
            file_path = os.path.join(CURRENT_DIR, "index.html")
        
        if request_path in [
            "/index.html",
            "/static/styles.css",
            "/static/codeboot.bundle.css",
            "/static/codeboot.bundle.js",
            "/interface.py",
            "/spreadsheet.py"
        ]:
            file_path = os.path.join(CURRENT_DIR, request_path.lstrip("/"))

        if file_path is None:
            self.send_error(404, "File not found")
            return

        try:
            with open(file_path, 'rb') as file:
                content = file.read()
        except OSError as exc:
            self.send_error(500, f"Cannot read file: {exc}")
            return

        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(file_path))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    handler = SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("localhost", PORT), handler)

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    print(f"Serving at port {PORT}")

    # Open the default web browser to the server's address
    webbrowser.open(f"http://localhost:{PORT}")

    try:
        server_thread.join()
    except KeyboardInterrupt:
        pass
