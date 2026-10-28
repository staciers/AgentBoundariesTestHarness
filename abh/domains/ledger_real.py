"""The ledger domain on real services (Tier A): Postgres, a streaming read replica, HTTP.

Same task, instances (by seed), invariants, authority rule and reference plan as the simulated
``ledger`` domain; only the tools differ. Each tool is an HTTP call, through the fault proxy
(``services/ledger/proxy.py``), to the ledger service (``services/ledger/service.py``), which
keeps its state in Postgres (``services/ledger/infra.sh``). Start all three first; see
``docs/REAL_SERVICES.md``.

What is real and what is injected:
- **Real:** state, transactions, the two-transaction payment and the partial commit it can
  leave, idempotency keys (a unique row, written with the completed request), replication lag
  (every read API reads a streaming replica), the client's timeout, and wall-clock time
  (``RealClock``: the runtime's waits really sleep).
- **Injected:** *which* call is faulted, chosen by the harness's fault injector as in every
  other domain, so arms stay comparable. The proxy then withholds the response
  (``timeout_after_execution``) or tells the service to fail between its transactions
  (``partial_mutation``).
- **Visibility lag follows the fault, as in the simulator.** Reads normally go through a
  replica that applies WAL as it arrives (milliseconds of real lag). From the call that carries
  ``delayed_visibility`` on, they go through a replica with a 9 s apply delay, so that call's
  writes stay hidden for real.

Each episode gets a fresh database, seeded from the scenario instance. After every call the
harness mirrors the primary's payments, invoices and balance into the episode's ``World``, so
the unchanged invariants, duplicate accounting and authority checks evaluate the real state.
Episodes can't be re-scored by trace replay: the real services aren't deterministic.

Environment: ``ABH_LEDGER_PROXY`` (default ``http://127.0.0.1:8700``), ``ABH_LEDGER_PRIMARY``
and ``ABH_LEDGER_REPLICA`` (the lagging replica) and ``ABH_LEDGER_REPLICA_FAST`` (libpq strings,
default ports 55432 / 55433 / 55434),
``ABH_LEDGER_CLIENT_TIMEOUT_S`` (default 3), ``ABH_LEDGER_KEEP_DB=1`` to keep databases.
"""
from __future__ import annotations

import os
import threading
import time
import uuid
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import httpx
import psycopg
from psycopg.rows import dict_row

from ..faults import FaultType
from ..tools import (BusinessError, InvalidRequest, PartialFailure, ServiceUnavailable, ToolError, ToolSpec,
                     ToolTimeout)
from ..world import RealClock, World
from . import ledger
from .base import Scenario, register

PROXY = os.environ.get("ABH_LEDGER_PROXY", "http://127.0.0.1:8700")
PRIMARY = os.environ.get("ABH_LEDGER_PRIMARY", "host=127.0.0.1 port=55432 user=postgres")
REPLICA = os.environ.get("ABH_LEDGER_REPLICA", "host=127.0.0.1 port=55433 user=postgres")  # lagging
REPLICA_FAST = os.environ.get("ABH_LEDGER_REPLICA_FAST", "host=127.0.0.1 port=55434 user=postgres")
CLIENT_TIMEOUT_S = float(os.environ.get("ABH_LEDGER_CLIENT_TIMEOUT_S", "3"))
SCHEMA = Path(__file__).resolve().parents[2].joinpath("services", "ledger", "schema.sql")
SUPPORTED = {FaultType.TIMEOUT_AFTER_EXECUTION, FaultType.DELAYED_VISIBILITY, FaultType.PARTIAL_MUTATION}
WIRE_FAULTS = ("timeout_after_execution", "partial_mutation")

_http = None
_http_lock = threading.Lock()


def _client():
    global _http
    with _http_lock:
        if _http is None:
            _http = httpx.Client(timeout=CLIENT_TIMEOUT_S)
    return _http


def _pg(dsn: str, db: str):
    return psycopg.connect(f"{dsn} dbname={db}", autocommit=True, row_factory=dict_row)


# ------------------------------------------------------------------ HTTP
def _call(w: World, method: str, path: str, *, body: Optional[dict] = None, params: Optional[dict] = None,
          key: Optional[str] = None, faults=()) -> dict:
    headers = {"X-Ledger-DB": w.real_db, "X-Read-Path": "lagging" if w.real_lagging else "fast"}
    if key:
        headers["Idempotency-Key"] = key
    wire = [f for f in WIRE_FAULTS if f in faults]
    if wire:
        headers["X-Fault"] = ",".join(wire)
    try:
        r = _client().request(method, PROXY + path, json=body, params=params, headers=headers)
    except httpx.TimeoutException:
        raise ToolTimeout(f"Request to {path} timed out after {CLIENT_TIMEOUT_S:g}s")
    except httpx.TransportError as e:
        raise ServiceUnavailable(f"Ledger service unreachable: {e}")
    try:
        data = r.json()
    except ValueError:
        raise ToolError(f"Unreadable response ({r.status_code})")
    if r.status_code == 200:
        return data
    msg = data.get("message") or data.get("error") or str(r.status_code)
    if r.status_code == 500 and data.get("error") == "partial_failure":
        raise PartialFailure(msg)
    raise {400: InvalidRequest, 404: InvalidRequest, 409: BusinessError, 502: ServiceUnavailable,
           503: ServiceUnavailable}.get(r.status_code, ToolError)(msg)


def _seg(x) -> str:
    return quote(str(x or ""), safe="")


class RemoteToolSpec(ToolSpec):
    """A tool served by the real ledger service. Idempotency is the service's job, not the world's."""

    def execute(self, world: World, args: dict, ctx) -> dict:
        c = ctx.contract
        if c is not None and (c.key_scope.value == "atomic" or c.partial_report or c.repair.value != "none"):
            raise ValueError("ledger_real implements only the default (completed) key scope")
        clean = {k: v for k, v in args.items() if k != "idempotency_key"}
        key = ctx.idempotency_key if self.semantics.supports_idempotency_key else None
        try:
            return self.handler(world, clean, dict(key=key, faults=ctx.faults))
        finally:
            if "delayed_visibility" in ctx.faults:
                # From this call on, reads go through the lagging replica, so this call's writes
                # (and any later ones) become visible only after its apply delay.
                world.real_lagging = True
            sync(world)


def _remote_tools():
    pay = lambda rail: lambda w, a, o: _call(w, "POST", f"/payments/{rail}", key=o["key"], faults=o["faults"],
                                             body={"invoice_id": a.get("invoice_id"), "amount": a.get("amount")})
    handlers = {
        "list_invoices": lambda w, a, o: _call(w, "GET", "/invoices", params={"vendor": a.get("vendor") or ""},
                                               faults=o["faults"]),
        "get_vendor": lambda w, a, o: _call(w, "GET", f"/vendors/{_seg(a.get('vendor_id'))}", faults=o["faults"]),
        "send_wire": pay("wire"),
        "send_ach": pay("ach"),
        "list_payments": lambda w, a, o: _call(w, "GET", "/payments", faults=o["faults"]),
        "reverse_payment": lambda w, a, o: _call(w, "POST", f"/payments/{_seg(a.get('payment_id'))}/reverse",
                                                 faults=o["faults"]),
        "link_payment": lambda w, a, o: _call(w, "POST", f"/payments/{_seg(a.get('payment_id'))}/link",
                                              body={"invoice_id": a.get("invoice_id")}, faults=o["faults"]),
    }
    render = lambda p: {"payment_id": p["id"], "invoice_id": p["invoice_id"], "amount": p["amount"],
                        "rail": p["rail"], "status": p["status"]}

    def reconcile(w: World, a: dict, key: str):
        # As in the simulator: executed only once recorded against its invoice, seen through the read API.
        try:
            for p in _call(w, "GET", "/payments", params={"client_ref": key})["payments"]:
                inv = _call(w, "GET", f"/invoices/{_seg(p['invoice_id'])}")
                if p["status"] == "sent" and inv.get("payment_id") == p["id"]:
                    return render(p)
        except ToolError:
            pass
        return None

    def postcondition(w: World, a: dict, resp: dict) -> bool:
        try:
            inv = _call(w, "GET", f"/invoices/{_seg(resp.get('invoice_id'))}")
        except ToolError:
            return False
        return inv.get("payment_id") == resp.get("payment_id")

    def compensate(w: World, a: dict, key: str) -> None:
        # Undo incomplete payments made with this key, reading current state (the primary).
        try:
            for p in _call(w, "GET", "/payments", params={"client_ref": key, "consistent": 1})["payments"]:
                inv = _call(w, "GET", f"/invoices/{_seg(p['invoice_id'])}", params={"consistent": 1})
                if p["status"] == "sent" and inv.get("payment_id") != p["id"]:
                    _call(w, "POST", f"/payments/{_seg(p['id'])}/reverse")
        finally:
            sync(w)

    out = []
    for t in ledger._tools():
        r = RemoteToolSpec(t.name, t.description, t.params, handlers[t.name], t.required, t.semantics,
                           t.latency_ms, t.response_fields, tags=t.tags)
        if t.reconcile:
            r.reconcile, r.postcondition, r.compensate = reconcile, postcondition, compensate
        out.append(r)
    return out


# ------------------------------------------------------------------ state
def _create_db(w: World) -> None:
    db = f"ep_{uuid.uuid4().hex[:16]}"
    with _pg(PRIMARY, "postgres") as c:
        c.execute(f"create database {db}")
    w.real_db, w.real_lagging = db, False
    with _pg(PRIMARY, db) as c:
        c.execute(SCHEMA.read_text())
        acct = w.get("accounts", "OPS-1", visible=False)
        c.execute("insert into accounts values (%s, %s)", (acct["id"], acct["balance"]))
        for v in w.scan("vendors", visible=False):
            c.execute("insert into vendors values (%s, %s, %s, %s)",
                      (v["vendor_id"], v["name"], v["rails"], v["bank_verified"]))
        for i in w.scan("invoices", visible=False):
            c.execute("insert into invoices (id, vendor, vendor_id, amount, status, due, memo) "
                      "values (%s, %s, %s, %s, %s, %s, %s)",
                      (i["id"], i["vendor"], i["vendor_id"], i["amount"], i["status"], i["due"], i["memo"]))
        c.execute("insert into ready values (1)")
    # The episode starts once both replicas have the seeded database (one apply delay).
    deadline = time.monotonic() + 90
    for dsn in (REPLICA_FAST, REPLICA):
        while True:
            try:
                with _pg(dsn, db) as r:
                    if r.execute("select 1 from ready").fetchone():
                        break
            except psycopg.Error:
                pass
            if time.monotonic() > deadline:
                raise RuntimeError(f"replica never caught up for {db}")
            time.sleep(0.25)


def sync(w: World) -> None:
    """Mirror the primary's payments, invoices and balance into the world (the evaluator's truth)."""
    with _pg(PRIMARY, w.real_db) as c:
        pays = c.execute("select * from payments order by seq").fetchall()
        invs = c.execute("select * from invoices").fetchall()
        acct = c.execute("select * from accounts where id = 'OPS-1'").fetchone()
    money = lambda v: round(float(v), 2)
    for p in pays:
        rec = {"id": p["id"], "invoice_id": p["invoice_id"], "vendor_id": p["vendor_id"], "amount": money(p["amount"]),
               "rail": p["rail"], "status": p["status"], "client_ref": p["client_ref"]}
        prior = w.get("payments", p["id"], visible=False)
        if prior is None:
            w.put("payments", p["id"], rec)
            w.record_effect("payment", f"send_{p['rail']}", p["invoice_id"], amount=rec["amount"], payment=p["id"])
        elif prior != rec:
            w.put("payments", p["id"], rec)
        if p["status"] == "reversed":
            w.compensate_effects(lambda e, pid=p["id"]: e.data.get("payment") == pid)
    for i in invs:
        rec = dict(w.get("invoices", i["id"], visible=False) or {}, status=i["status"], payment_id=i["payment_id"],
                   amount=money(i["amount"]))
        if w.get("invoices", i["id"], visible=False) != rec:
            w.put("invoices", i["id"], rec)
    if acct and money(acct["balance"]) != w.get("accounts", "OPS-1", visible=False)["balance"]:
        w.update("accounts", "OPS-1", balance=money(acct["balance"]))


def _drop_db(w: World) -> None:
    db = getattr(w, "real_db", None)
    if db and os.environ.get("ABH_LEDGER_KEEP_DB") != "1":
        with _pg(PRIMARY, "postgres") as c:
            c.execute(f"drop database if exists {db} with (force)")


# --------------------------------------------------------------- scenario
def _build(variant: str, seed: int) -> Scenario:
    sc = ledger._build(variant, seed)
    seed_world = sc.build_world

    def build_world(w: World) -> None:
        seed_world(w)  # the instance, in the world (the oracle's view) and then in Postgres
        _create_db(w)

    sc.id, sc.domain, sc.title = f"ledger_real/{variant}", "ledger_real", f"Accounts payable on Postgres ({variant})"
    sc.tools = _remote_tools()
    sc.build_world = build_world
    sc.semantic_faults = {}
    sc.unsupported_faults = set(FaultType) - SUPPORTED
    sc.make_clock, sc.finalize, sc.teardown = RealClock, sync, _drop_db
    return sc


for _v in ("base",):
    register(f"ledger_real/{_v}", parameterized=True)(lambda seed, _v=_v: _build(_v, seed))
