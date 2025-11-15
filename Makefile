.PHONY: help setup dev-up dev-down migrate seed clean update-data

help:
	@echo "Available commands:"
	@echo "  make setup       - Set up development environment"
	@echo "  make dev-up      - Start all services with Docker Compose"
	@echo "  make dev-down    - Stop all services"
	@echo "  make migrate     - Run database migrations"
	@echo "  make seed        - Seed database with initial data"
	@echo "  make update-data - Update with realistic outbreak data"
	@echo "  make clean       - Clean up Docker volumes and containers"

setup:
	@echo "Setting up development environment..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev-up:
	docker compose up -d || docker-compose up -d
	@echo "Waiting for database to be ready..."
	sleep 5
	make migrate

dev-down:
	docker compose down || docker-compose down

migrate:
	docker compose exec backend alembic upgrade head || docker-compose exec backend alembic upgrade head

seed:
	docker compose exec backend python scripts/seed_data.py || docker-compose exec backend python scripts/seed_data.py

update-data:
	@echo "Updating with realistic outbreak data..."
	cd backend && venv/bin/python scripts/update_realistic_data.py

clean:
	docker compose down -v || docker-compose down -v
	docker system prune -f

