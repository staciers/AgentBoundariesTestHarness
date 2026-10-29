"""Accounts-payable ledger service over Postgres (Tier A real-services replication).

    .venv/bin/python services/ledger/service.py [--port 8701]

The same business rules as the simulated ``ledger`` domain (``abh/domains/ledger.py``), on
real infrastructure:

- **State** is in Postgres. Each episode has its own database, named in the
  ``X-Ledger-DB`` header.
- **Reads go through a streaming read replica**, so a committed write becomes visible to
  readers only after real replication lag. ``X-Read-Path: lagging`` selects the replica with
  ``recovery_min_apply_delay`` (set by ``infra.sh``); otherwise reads use the replica that
  applies WAL as it arrives. Calls that must see current state (the payment service's own key
  and balance checks, and ``consistent=1`` reads the runtime uses for compensation) read the
  primary.
- **A payment is two transactions:** debit and record the payment, then mark the invoice paid.
  A crash between them leaves a real partial commit. ``X-Inject-Partial: 1`` (set by the fault
  proxy) makes the service fail at that point.
- **Idempotency keys** (``Idempotency-Key``) are rows in ``idempotency_keys``, written in the
  same transaction as the invoice update. That is the *completed* key scope the simulated
  contract declares: a key is recorded only when the request completes, so a retry after a
  partial commit runs again. Requests with the same key are serialized with an advisory lock.

Errors use HTTP status codes that the harness maps back to its tool errors: 400 invalid
request, 409 business rejection, 500 partial failure (body ``"error": "partial_failure"``).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import threading
import zlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import psycopg
from psycopg.rows import dict_row

PRIMARY = os.environ.get("ABH_LEDGER_PRIMARY", "host=127.0.0.1 port=55432 user=postgres")
REPLICA = os.environ.get("ABH_LEDGER_REPLICA", "host=127.0.0.1 port=55433 user=postgres")  # lagging
REPLICA_FAST = os.environ.get("ABH_LEDGER_REPLICA_FAST", "host=127.0.0.1 port=55434 user=postgres")
_request = threading.local()


def read_dsn() -> str:
    """The replica this request reads through: the lagging one only when the caller asks for it."""
    return REPLICA if getattr(_request, "read_path", "fast") == "lagging" else REPLICA_FAST

SCHEMA = (Path(__file__).with_name("schema.sql")).read_text()


class HttpError(Exception):
    def __init__(self, status: int, error: str, message: str):
        super().__init__(message)
        self.status, self.error, self.message = status, error, message


def connect(dsn: str, db: str):
    return psycopg.connect(f"{dsn} dbname={db}", autocommit=True, row_factory=dict_row)


def money(v) -> float:
    return round(float(v), 2)


def public_invoice(r: dict) -> dict:
    return {"id": r["id"], "vendor": r["vendor"], "vendor_id": r["vendor_id"], "amount": money(r["amount"]),
            "status": r["status"], "due": r["due"], "memo": r["memo"]}


def public_payment(r: dict) -> dict:
    return {"id": r["id"], "invoice_id": r["invoice_id"], "vendor_id": r["vendor_id"], "amount": money(r["amount"]),
            "rail": r["rail"], "status": r["status"]}


def parse_amount(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


# ------------------------------------------------------------------ handlers
def list_invoices(db: str, q: dict) -> dict:
    vendor = (q.get("vendor") or "").strip().lower()
    with connect(read_dsn(), db) as c:
        rows = c.execute("select * from invoices order by id").fetchall()
    return {"invoices": [public_invoice(r) for r in rows if not vendor or r["vendor"].lower() == vendor]}


def get_invoice(db: str, invoice_id: str, q: dict) -> dict:
    with connect(PRIMARY if q.get("consistent") else read_dsn(), db) as c:
        r = c.execute("select * from invoices where id = %s", (invoice_id,)).fetchone()
    if r is None:
        raise HttpError(400, "invalid_request", f"Unknown invoice {invoice_id}")
    return dict(public_invoice(r), payment_id=r["payment_id"])


def get_vendor(db: str, vendor_id: str) -> dict:
    with connect(read_dsn(), db) as c:
        r = c.execute("select * from vendors where vendor_id = %s", (vendor_id,)).fetchone()
    if r is None:
        raise HttpError(400, "invalid_request", f"Unknown vendor {vendor_id}")
    return {"vendor_id": r["vendor_id"], "name": r["name"], "rails": list(r["rails"]),
            "bank_verified": r["bank_verified"]}


def list_payments(db: str, q: dict) -> dict:
    sql, args = "select * from payments", []
    if q.get("client_ref"):
        sql, args = sql + " where client_ref = %s", [q["client_ref"]]
    with connect(PRIMARY if q.get("consistent") else read_dsn(), db) as c:
        rows = c.execute(sql + " order by seq", args).fetchall()
    return {"payments": [public_payment(r) for r in rows]}


def send_payment(db: str, rail: str, body: dict, key: str | None, inject_partial: bool) -> dict:
    endpoint = f"send_{rail}"
    with connect(PRIMARY, db) as p:
        if key:  # serialize requests that share a key, for the whole request
            p.execute("select pg_advisory_lock(%s)", (zlib.crc32(f"{endpoint}:{key}".encode()),))
        try:
            if key:
                prior = p.execute("select response from idempotency_keys where endpoint = %s and key = %s",
                                  (endpoint, key)).fetchone()
                if prior is not None:
                    return prior["response"]
            return _send_once(db, p, rail, endpoint, body, key, inject_partial)
        finally:
            if key:
                p.execute("select pg_advisory_unlock_all()")


def _send_once(db, p, rail, endpoint, body, key, inject_partial) -> dict:
    invoice_id = body.get("invoice_id") or ""
    with connect(read_dsn(), db) as r:  # the payment service checks the invoice through the ledger's read API
        inv = r.execute("select * from invoices where id = %s", (invoice_id,)).fetchone()
    if inv is None:
        raise HttpError(400, "invalid_request", f"Unknown invoice {invoice_id}")
    if inv["status"] == "paid":
        raise HttpError(409, "business_error", f"Invoice {inv['id']} is already paid")
    if inv["status"] != "approved":
        raise HttpError(409, "business_error",
                        f"Invoice {inv['id']} is not approved for payment (status: {inv['status']})")
    amount = parse_amount(body.get("amount", 0))
    if amount is None:
        raise HttpError(400, "invalid_request", f"Amount must be a number, got {body.get('amount')!r}")
    amount = round(amount, 2)
    if abs(amount - money(inv["amount"])) > 0.005:
        raise HttpError(409, "business_error", f"Amount {amount:.2f} does not match the balance of invoice {inv['id']}")

    # Transaction 1: debit the account and record the payment (the external effect).
    with p.transaction():
        p.execute("update accounts set balance = balance - %s where id = 'OPS-1'", (amount,))
        seq = p.execute("select nextval('payment_seq') as n").fetchone()["n"]
        pid = f"PAY{seq:04d}"
        p.execute("insert into payments (id, seq, invoice_id, vendor_id, amount, rail, status, client_ref) "
                  "values (%s, %s, %s, %s, %s, %s, 'sent', %s)", (pid, seq, inv["id"], inv["vendor_id"], amount, rail, key))
    if inject_partial:
        raise HttpError(500, "partial_failure", f"Payment {pid} was sent, but invoice {inv['id']} could not be "
                                                "marked paid; the ledger is out of sync")
    # Transaction 2: mark the invoice paid, and record the key (completed scope).
    resp = {"payment_id": pid, "invoice_id": inv["id"], "amount": amount, "rail": rail, "status": "sent"}
    with p.transaction():
        p.execute("update invoices set status = 'paid', payment_id = %s where id = %s", (pid, inv["id"]))
        if key:
            p.execute("insert into idempotency_keys (endpoint, key, response) values (%s, %s, %s)",
                      (endpoint, key, json.dumps(resp)))
    return resp


def inspect_attempt(db: str, q: dict) -> dict:
    """How far the payment made with a key got: complete, partial or absent, from the primary.

    Takes the key's lock first, so an attempt with that key that is still executing finishes
    before the answer is read: the answer can't be overtaken by a commit in flight.
    """
    endpoint, key = q.get("endpoint") or "", q.get("key") or ""
    if endpoint not in ("send_wire", "send_ach") or not key:
        raise HttpError(400, "invalid_request", "endpoint (send_wire or send_ach) and key are required")
    with connect(PRIMARY, db) as p:
        p.execute("select pg_advisory_lock(%s)", (zlib.crc32(f"{endpoint}:{key}".encode()),))
        try:
            pays = p.execute("select p.id, i.payment_id as linked from payments p left join invoices i "
                             "on i.id = p.invoice_id where p.client_ref = %s and p.status = 'sent'", (key,)).fetchall()
        finally:
            p.execute("select pg_advisory_unlock_all()")
    status = "absent" if not pays else "complete" if any(r["linked"] == r["id"] for r in pays) else "partial"
    return {"key": key, "status": status}


def reverse_payment(db: str, payment_id: str) -> dict:
    with connect(PRIMARY, db) as p, p.transaction():
        pay = p.execute("select * from payments where id = %s for update", (payment_id,)).fetchone()
        if pay is None:
            raise HttpError(400, "invalid_request", "Unknown payment")
        if pay["status"] != "reversed":
            p.execute("update accounts set balance = balance + %s where id = 'OPS-1'", (pay["amount"],))
            p.execute("update payments set status = 'reversed' where id = %s", (payment_id,))
            p.execute("update invoices set status = 'approved', payment_id = null "
                      "where id = %s and payment_id = %s", (pay["invoice_id"], payment_id))
    return {"payment_id": payment_id, "status": "reversed"}


def link_payment(db: str, payment_id: str, body: dict) -> dict:
    invoice_id = body.get("invoice_id") or ""
    with connect(PRIMARY, db) as p, p.transaction():
        pay = p.execute("select * from payments where id = %s for update", (payment_id,)).fetchone()
        inv = p.execute("select * from invoices where id = %s for update", (invoice_id,)).fetchone()
        if pay is None or inv is None:
            raise HttpError(400, "invalid_request", "Unknown payment or invoice")
        if pay["status"] != "sent" or pay["invoice_id"] != inv["id"]:
            raise HttpError(409, "business_error", "That payment can't be linked to that invoice")
        if inv["status"] == "paid" and inv["payment_id"] not in (None, pay["id"]):
            raise HttpError(409, "business_error", f"Invoice {inv['id']} is already paid by another payment")
        p.execute("update invoices set status = 'paid', payment_id = %s where id = %s", (pay["id"], inv["id"]))
    return {"invoice_id": inv["id"], "status": "paid", "payment_id": pay["id"]}


# ------------------------------------------------------------------ HTTP
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # quiet; the proxy keeps the request log
        pass

    def _reply(self, status: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _route(self, method: str) -> None:
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        parts = [x for x in url.path.split("/") if x]
        db = self.headers.get("X-Ledger-DB", "")
        _request.read_path = self.headers.get("X-Read-Path", "fast")
        body = {}
        if method == "POST":
            n = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(n) or b"{}")
            except json.JSONDecodeError:
                return self._reply(400, {"error": "invalid_request", "message": "Body is not valid JSON"})
        try:
            if not db.startswith("ep_"):
                raise HttpError(400, "invalid_request", "Missing or invalid X-Ledger-DB")
            if method == "GET" and parts == ["invoices"]:
                out = list_invoices(db, q)
            elif method == "GET" and len(parts) == 2 and parts[0] == "invoices":
                out = get_invoice(db, parts[1], q)
            elif method == "GET" and len(parts) == 2 and parts[0] == "vendors":
                out = get_vendor(db, parts[1])
            elif method == "GET" and parts == ["payments"]:
                out = list_payments(db, q)
            elif method == "GET" and parts == ["payments", "attempts"]:
                out = inspect_attempt(db, q)
            elif method == "POST" and len(parts) == 2 and parts[0] == "payments" and parts[1] in ("wire", "ach"):
                out = send_payment(db, parts[1], body, self.headers.get("Idempotency-Key"),
                                   self.headers.get("X-Inject-Partial") == "1")
            elif method == "POST" and len(parts) == 3 and parts[0] == "payments" and parts[2] == "reverse":
                out = reverse_payment(db, parts[1])
            elif method == "POST" and len(parts) == 3 and parts[0] == "payments" and parts[2] == "link":
                out = link_payment(db, parts[1], body)
            else:
                raise HttpError(404, "not_found", f"No route for {method} {url.path}")
        except HttpError as e:
            return self._reply(e.status, {"error": e.error, "message": e.message})
        except psycopg.OperationalError as e:
            return self._reply(503, {"error": "unavailable", "message": f"database unavailable: {e}"})
        self._reply(200, out)

    def do_GET(self):
        self._route("GET")

    def do_POST(self):
        self._route("POST")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8701)
    args = ap.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.daemon_threads = True
    print(f"ledger service on 127.0.0.1:{args.port} (primary: {PRIMARY}; replicas: fast {REPLICA_FAST}, lagging {REPLICA})", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
