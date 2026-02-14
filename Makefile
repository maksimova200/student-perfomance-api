up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v

logs:
	docker logs service-postgres

status:
	docker ps

tests:
	docker compose run --rm --build app python -m pytest tests/ -v


.PHONY: up down clean logs status tests start