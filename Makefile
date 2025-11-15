.PHONY: help setup dev-up dev-down migrate seed clean

help:
	@echo "Available commands:"
	@echo "  make setup      - Set up development environment"
	@echo "  make dev-up     - Start all services with Docker Compose"
	@echo "  make dev-down   - Stop all services"
	@echo "  make migrate    - Run database migrations"
	@echo "  make seed       - Seed database with sample data"
	@echo "  make clean      - Clean up Docker volumes and containers"

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

clean:
	docker compose down -v || docker-compose down -v
	docker system prune -f

