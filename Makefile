up:
	docker compose up --d

down:
	docker compose down

clean: down
	sudo rm -rf ./.pgdata

logs:
	docker logs service-postgres

status:
	docker ps

.PHONY: up down clean logs status