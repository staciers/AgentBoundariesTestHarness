#!/usr/bin/env bash
# The whole real-services ledger stack: Postgres primary + two replicas, service, fault proxy.
#
#   services/ledger/stack.sh up            # infra (if not running), service, proxy
#   services/ledger/stack.sh status
#   services/ledger/stack.sh fresh-log     # restart the proxy with a new log (do this before each run)
#   services/ledger/stack.sh collect <run_dir>   # copy the stack record and proxy log into a run
#   services/ledger/stack.sh down          # stop service and proxy, remove the containers
#
# Settings (environment): APPLY_DELAY (replica delay, default 9s), PROXY_HOLD_S (default 6),
# SERVICE_PORT (8701), PROXY_PORT (8700). The harness's client timeout is
# ABH_LEDGER_CLIENT_TIMEOUT_S (default 3), which must stay below PROXY_HOLD_S.
set -euo pipefail
cd "$(dirname "$0")/../.."

HERE=services/ledger
STATE="$HERE/.run"
PY=.venv/bin/python
APPLY_DELAY="${APPLY_DELAY:-9s}"
PROXY_HOLD_S="${PROXY_HOLD_S:-6}"
SERVICE_PORT="${SERVICE_PORT:-8701}"
PROXY_PORT="${PROXY_PORT:-8700}"

running() { [[ -f "$STATE/$1.pid" ]] && kill -0 "$(cat "$STATE/$1.pid")" 2>/dev/null; }

up() {
  mkdir -p "$STATE"
  docker inspect -f '{{.State.Running}}' abh-pg-replica-fast 2>/dev/null | grep -q true || "$HERE/infra.sh" up "$APPLY_DELAY"
  local stamp; stamp="$(date +%Y%m%d-%H%M%S)"
  if ! running service; then
    nohup "$PY" "$HERE/service.py" --port "$SERVICE_PORT" > "$STATE/service.log" 2>&1 &
    echo $! > "$STATE/service.pid"
  fi
  if ! running proxy; then
    nohup "$PY" "$HERE/proxy.py" --port "$PROXY_PORT" --upstream "http://127.0.0.1:$SERVICE_PORT" \
      --hold "$PROXY_HOLD_S" --log "$STATE/proxy-$stamp-$$.jsonl" > "$STATE/proxy.log" 2>&1 &
    echo $! > "$STATE/proxy.pid"
    echo "$STATE/proxy-$stamp-$$.jsonl" > "$STATE/proxy-log-path"
  fi
  for _ in $(seq 1 40); do
    curl -s -o /dev/null "http://127.0.0.1:$PROXY_PORT/invoices" && break
    sleep 0.25
  done
  record > "$STATE/stack.json"
  status
}

record() {
  cat <<EOF
{
  "recorded_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "git_commit": "$(git rev-parse HEAD)",
  "git_clean": $(git diff --quiet -- services abh && echo true || echo false),
  "postgres_image": "$(docker image inspect postgres:16 --format '{{index .RepoDigests 0}}')",
  "postgres_version": "$(docker exec abh-pg-primary psql -U postgres -tAc 'show server_version')",
  "replica_apply_delay": "$(docker exec abh-pg-replica psql -U postgres -tAc 'show recovery_min_apply_delay')",
  "fast_replica_apply_delay": "$(docker exec abh-pg-replica-fast psql -U postgres -tAc 'show recovery_min_apply_delay')",
  "proxy_hold_s": $PROXY_HOLD_S,
  "client_timeout_s": ${ABH_LEDGER_CLIENT_TIMEOUT_S:-3},
  "service_port": $SERVICE_PORT,
  "proxy_port": $PROXY_PORT,
  "proxy_log": "$(cat "$STATE/proxy-log-path" 2>/dev/null)"
}
EOF
}

status() {
  "$HERE/infra.sh" status
  running service && echo "service: pid $(cat "$STATE/service.pid") on 127.0.0.1:$SERVICE_PORT" || echo "service: not running"
  running proxy && echo "proxy: pid $(cat "$STATE/proxy.pid") on 127.0.0.1:$PROXY_PORT, log $(cat "$STATE/proxy-log-path")" \
    || echo "proxy: not running"
}

fresh_log() {
  running proxy && kill "$(cat "$STATE/proxy.pid")" || true
  rm -f "$STATE/proxy.pid"
  up >/dev/null
  echo "proxy log: $(cat "$STATE/proxy-log-path")"
}

collect() {
  local run="${1:?usage: stack.sh collect <run_dir>}"
  cp "$STATE/stack.json" "$run/stack.json"
  cp "$(cat "$STATE/proxy-log-path")" "$run/proxy.jsonl"
  echo "copied stack.json and proxy.jsonl into $run"
}

down() {
  for p in proxy service; do
    running "$p" && kill "$(cat "$STATE/$p.pid")" || true
    rm -f "$STATE/$p.pid"
  done
  "$HERE/infra.sh" down
}

case "${1:-}" in
  up) up ;;
  status) status ;;
  fresh-log) fresh_log ;;
  collect) shift; collect "$@" ;;
  down) down ;;
  *) echo "usage: $0 up | status | fresh-log | collect <run_dir> | down" >&2; exit 2 ;;
esac
