#!/usr/bin/env bash
set -Eeuo pipefail
dc="docker compose -f compose/docker-compose.yml -f compose/docker-compose.override.yml"

echo "==> Upgrading metadata DB and re-initializing..."
$dc exec superset superset db upgrade
$dc exec superset superset init
echo "==> Upgrade complete."
