#!/usr/bin/env bash
set -Eeuo pipefail

dc="docker compose -f compose/docker-compose.yml -f compose/docker-compose.override.yml"

echo "==> Waiting for Superset to be healthy..."
$dc ps
$dc wait superset || true

echo "==> Running initial DB upgrade..."
$dc exec superset superset db upgrade

echo "==> Creating admin user..."
req=(SUPERSET_ADMIN_USERNAME SUPERSET_ADMIN_PASSWORD SUPERSET_ADMIN_FIRST_NAME SUPERSET_ADMIN_LAST_NAME SUPERSET_ADMIN_EMAIL)
for v in "${req[@]}"; do
  if ! $dc exec superset sh -lc "[ -n \"\${$v}\" ]"; then
    echo "Missing $v in env files."; exit 1
  fi
done

$dc exec superset superset fab create-admin \
  --username "$($dc exec -T superset sh -lc 'echo -n $SUPERSET_ADMIN_USERNAME')" \
  --firstname "$($dc exec -T superset sh -lc 'echo -n $SUPERSET_ADMIN_FIRST_NAME')" \
  --lastname "$($dc exec -T superset sh -lc 'echo -n $SUPERSET_ADMIN_LAST_NAME')" \
  --email "$($dc exec -T superset sh -lc 'echo -n $SUPERSET_ADMIN_EMAIL')" \
  --password "$($dc exec -T superset sh -lc 'echo -n $SUPERSET_ADMIN_PASSWORD')"

echo "==> Running superset init..."
$dc exec superset superset init

echo "==> Done. Open http://localhost:${SUPERSET_PORT:-8088}"
