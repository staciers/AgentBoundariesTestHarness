#!/usr/bin/env bash
# Postgres primary + two streaming read replicas for the real-services ledger (Tier A).
#
#   services/ledger/infra.sh up [apply_delay]   # default 9s: the 3s client timeout + the simulator's 6s delay_ms
#   services/ledger/infra.sh down
#   services/ledger/infra.sh status
#
# Both replicas stream WAL from the primary, so both lag it for real:
# - the *fast* replica applies WAL as it arrives (milliseconds of lag): the normal read path
# - the *lagging* replica waits `recovery_min_apply_delay` after each commit: the read path
#   under a `delayed_visibility` fault
# Ports bind to 127.0.0.1 only, with trust auth: a local test database, never exposed.
set -euo pipefail

IMAGE=postgres:16
NET=abh-ledger
PRIMARY=abh-pg-primary
LAGGING=abh-pg-replica
FAST=abh-pg-replica-fast
PRIMARY_PORT=55432
LAGGING_PORT=55433
FAST_PORT=55434

replica() {  # replica <container> <port> <apply delay>
  docker run -d --name "$1" --network "$NET" -p "127.0.0.1:$2:5432" \
    -e POSTGRES_HOST_AUTH_METHOD=trust --entrypoint bash "$IMAGE" -c "
      set -e
      rm -rf \"\$PGDATA\"/* 2>/dev/null || true
      until pg_basebackup -h $PRIMARY -U postgres -D \"\$PGDATA\" -X stream -R; do sleep 1; done
      echo \"recovery_min_apply_delay = '$3'\" >> \"\$PGDATA/postgresql.auto.conf\"
      echo \"hot_standby = on\" >> \"\$PGDATA/postgresql.auto.conf\"
      echo \"max_connections = 300\" >> \"\$PGDATA/postgresql.auto.conf\"
      chown -R postgres:postgres \"\$PGDATA\"; chmod 700 \"\$PGDATA\"
      exec gosu postgres postgres" >/dev/null
}

up() {
  local delay="${1:-9s}"
  docker network inspect "$NET" >/dev/null 2>&1 || docker network create "$NET" >/dev/null
  docker run -d --name "$PRIMARY" --network "$NET" -p "127.0.0.1:${PRIMARY_PORT}:5432" \
    -e POSTGRES_HOST_AUTH_METHOD=trust "$IMAGE" \
    -c wal_level=replica -c max_wal_senders=10 -c max_connections=300 \
    -c synchronous_commit=on -c fsync=on >/dev/null
  until docker exec "$PRIMARY" pg_isready -U postgres -q; do sleep 0.5; done
  # pg_isready can pass during the image's init restart; wait for a real query.
  until docker exec "$PRIMARY" psql -U postgres -tAc "select 1" >/dev/null 2>&1; do sleep 0.5; done
  docker exec "$PRIMARY" bash -c "echo 'host replication all all trust' >> \"\$PGDATA/pg_hba.conf\""
  docker exec "$PRIMARY" psql -U postgres -qc "select pg_reload_conf()" >/dev/null

  replica "$LAGGING" "$LAGGING_PORT" "$delay"
  replica "$FAST" "$FAST_PORT" 0
  for r in "$LAGGING" "$FAST"; do
    until docker exec "$r" psql -U postgres -tAc "select pg_is_in_recovery()" 2>/dev/null | grep -q t; do
      sleep 0.5
    done
  done
  status
}

down() {
  docker rm -f "$FAST" "$LAGGING" "$PRIMARY" >/dev/null 2>&1 || true
  docker network rm "$NET" >/dev/null 2>&1 || true
  echo "ledger infrastructure removed"
}

status() {
  echo "primary: $(docker exec "$PRIMARY" psql -U postgres -tAc 'select version()' | cut -d, -f1) on 127.0.0.1:${PRIMARY_PORT}"
  for r in "$LAGGING:$LAGGING_PORT" "$FAST:$FAST_PORT"; do
    local c="${r%%:*}" p="${r##*:}"
    echo "replica $c: in recovery=$(docker exec "$c" psql -U postgres -tAc 'select pg_is_in_recovery()')," \
         "apply delay=$(docker exec "$c" psql -U postgres -tAc 'show recovery_min_apply_delay') on 127.0.0.1:$p"
  done
  echo "image: $(docker image inspect "$IMAGE" --format '{{index .RepoDigests 0}}')"
}

case "${1:-}" in
  up) shift; up "$@" ;;
  down) down ;;
  status) status ;;
  *) echo "usage: $0 up [apply_delay] | down | status" >&2; exit 2 ;;
esac
