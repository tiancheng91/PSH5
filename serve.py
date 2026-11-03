import http.server
import socket
import sys
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).resolve().parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, *args):
        pass

    def do_GET(self):
        path = (self.path or "").split("?", 1)[0]
        if path == "/cache.appcache" or path == "/offline.appcache":
            self.send_error(404, "obsolete")
            return
        return super().do_GET()

    def guess_type(self, path):
        if str(path).endswith(".appcache"):
            return "text/cache-manifest"
        return super().guess_type(path)

    def end_headers(self):
        path = (self.path or "").split("?", 1)[0]
        self.send_header("Access-Control-Allow-Origin", "*")
        if path.endswith(".appcache") or path.endswith(".js"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

def local_ip():
    addresses = []
    if sys.platform.startswith("linux"):
        # Query every interface, including LAN interfaces absent from DNS.
        import fcntl
        import struct

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                for _, name in socket.if_nameindex():
                    try:
                        request = struct.pack("256s", name.encode()[:15])
                        result = fcntl.ioctl(sock.fileno(), 0x8915, request)  # SIOCGIFADDR
                        addresses.append(socket.inet_ntoa(result[20:24]))
                    except OSError:
                        continue
        except OSError:
            pass
    try:
        addresses.extend(info[4][0] for info in socket.getaddrinfo(
            socket.gethostname(), None, socket.AF_INET, socket.SOCK_STREAM
        ))
    except OSError:
        pass

    return next((ip for ip in addresses if ip.startswith("192.168.")), "127.0.0.1")

if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as server:
        print(f"http://127.0.0.1:{PORT}/")
        server.serve_forever()