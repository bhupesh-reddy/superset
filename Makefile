COMPOSE_BASE=compose/docker-compose.yml
COMPOSE_LOCAL=compose/docker-compose.override.yml
COMPOSE_PROD=compose/docker-compose.prod.yml

.PHONY: up down logs init upgrade ps restart clean prod-up

up:
	docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) up -d --wait

down:
	docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) down

logs:
	docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) logs -f superset

init: up
	./scripts/first-run.sh

upgrade:
	./scripts/upgrade.sh

ps:
	docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) ps

restart:
	docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) restart superset

clean:
	@read -p "This removes named volumes (DATA WILL BE LOST). Continue? [y/N] " ans; \
	if [ "$$ans" = "y" ]; then \
		docker volume rm org-superset_pg_data || true; \
		docker volume rm org-superset_superset_home || true; \
	fi

prod-up:
	docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_PROD) up -d --wait
