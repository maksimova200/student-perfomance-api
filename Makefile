build:
	docker compose up --build

up:
	docker compose up -d

down:
	docker compose down

clean: down
	sudo rm -rf ./.pgdata

logs:
	docker logs service-postgres

status:
	docker ps

tests:
	docker compose run --rm --build app python -m pytest tests/ -v


.PHONY: up down clean logs status tests start