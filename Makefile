.PHONY: up down migrate seed test lint typecheck prefect-ui

up:
	docker compose up --build -d

down:
	docker compose down

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec db psql -U geoetl -d geoetl -f /app/sample_data/seed.sql

test:
	docker compose exec backend pytest

lint:
	docker compose exec backend ruff app && docker compose exec backend black --check app && docker compose exec backend isort --check-only app

typecheck:
	docker compose exec backend mypy app

prefect-ui:
	docker compose exec prefect prefect server start
