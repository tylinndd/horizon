.PHONY: help setup dev-up dev-down migrate seed clean update-data update-data-simulated prefect-register ingest-local hackathon-prep

help:
	@echo "Available commands:"
	@echo "  make setup          - Set up development environment"
	@echo "  make dev-up         - Start all services with Docker Compose"
	@echo "  make dev-down       - Stop all services"
	@echo "  make migrate        - Run database migrations"
	@echo "  make seed           - Seed database with initial data"
	@echo "  make update-data    - Update with realistic outbreak data"
	@echo "  make hackathon-prep - Prepare for hackathon demo (hybrid: real + mock)"
	@echo "  make clean          - Clean up Docker volumes and containers"

setup:
	@echo "Setting up development environment..."
	cd backend && python3.11 -m venv venv && venv/bin/pip install -r requirements.txt
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
	@echo "Updating with real outbreak data (OWID + Google Trends)..."
	cd backend && venv/bin/python scripts/fetch_real_data.py

update-data-simulated:
	@echo "Updating with realistic simulated outbreak data..."
	cd backend && venv/bin/python scripts/update_realistic_data.py

prefect-register:
	@echo "Registering Prefect deployments for data ingestion..."
	cd backend && venv/bin/python scripts/register_prefect_deployments.py

ingest-local:
	@echo "Ingesting local CSV datasets into Horizon..."
	cd backend && venv/bin/python scripts/ingest_local_datasets.py

hackathon-prep:
	@echo "Preparing Horizon for hackathon demo..."
	cd backend && venv/bin/python scripts/prepare_hackathon_demo.py --mode hybrid --include-local

mock-data-extensive:
	@echo "Generating extensive realistic mock data..."
	cd backend && venv/bin/python scripts/generate_extensive_mock_data.py

clean:
	docker compose down -v || docker-compose down -v
	docker system prune -f

