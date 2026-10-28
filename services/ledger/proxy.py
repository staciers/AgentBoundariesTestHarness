"""Fault-injecting HTTP proxy in front of the ledger service (Tier A).

    .venv/bin/python services/ledger/proxy.py [--port 8700] [--upstream http://127.0.0.1:8701]
                                              [--hold 6] [--log runs/<dir>/proxy.jsonl]

The harness's fault injector decides *which* call is faulted (so arms stay comparable) and
names the faults in the ``X-Fault`` header. The proxy makes them happen on the wire:

- ``timeout_after_execution``: the request is forwarded and the service executes it, but the
  proxy withholds the response and holds the connection open for ``--hold`` seconds. The
  client's own read timeout (shorter than the hold) fires, so the client really can't tell
  whether its request executed.
- ``partial_mutation``: forwarded with ``X-Inject-Partial: 1``, so the service fails between
  its two transactions, leaving a real partial commit in the database.

Every request is logged (episode database, method, path, faults, upstream status, whether
the response was withheld), as evidence of what the client saw.
"""
from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx

ARGS = None
_log_lock = threading.Lock()
_client = None


def log(entry: dict) -> None:
    if not ARGS.log:
        return
    with _log_lock, open(ARGS.log, "a") as f:
        f.write(json.dumps(entry) + "\n")


class Proxy(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def _forward(self, method: str) -> None:
        faults = {f.strip() for f in (self.headers.get("X-Fault") or "").split(",") if f.strip()}
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in ("host", "content-length", "x-fault", "connection")}
        if "partial_mutation" in faults:
            headers["X-Inject-Partial"] = "1"
        t0 = time.time()
        entry = {"t": t0, "db": self.headers.get("X-Ledger-DB"), "method": method, "path": self.path,
                 "faults": sorted(faults), "key": self.headers.get("Idempotency-Key")}
        try:
            up = _client.request(method, ARGS.upstream + self.path, content=body, headers=headers)
        except httpx.HTTPError as e:
            log(dict(entry, upstream_status=None, error=str(e)))
            return self._send(502, b'{"error": "unavailable", "message": "bad gateway"}')
        entry.update(upstream_status=up.status_code, upstream_ms=round((time.time() - t0) * 1000))
        if "timeout_after_execution" in faults:
            # The service has executed and answered; the client never gets that answer.
            log(dict(entry, withheld=True))
            time.sleep(ARGS.hold)
            self.close_connection = True
            return
        log(dict(entry, withheld=False))
        self._send(up.status_code, up.content)

    def _send(self, status: int, data: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._forward("GET")

    def do_POST(self):
        self._forward("POST")


def main() -> None:
    global ARGS, _client
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8700)
    ap.add_argument("--upstream", default="http://127.0.0.1:8701")
    ap.add_argument("--hold", type=float, default=6.0, help="seconds to hold a withheld response's connection")
    ap.add_argument("--log", default=None)
    ARGS = ap.parse_args()
    _client = httpx.Client(timeout=30.0)
    server = ThreadingHTTPServer(("127.0.0.1", ARGS.port), Proxy)
    server.daemon_threads = True
    print(f"fault proxy on 127.0.0.1:{ARGS.port} -> {ARGS.upstream}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
