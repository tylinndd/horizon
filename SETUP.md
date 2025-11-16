# Horizon Setup Guide

This guide will help you set up and run the Horizon application.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15+ with TimescaleDB extension (if running locally)

## Quick Start with Docker

1. **Clone and navigate to the project:**
```bash
cd horizon
```

2. **Set up environment variables:**
```bash
cd backend
cp .env.example .env
# Edit .env and add your OpenRouter API key (optional for basic functionality)
```

3. **Start all services:**
```bash
docker compose up -d
```
   (Note: Use `docker-compose` if you have an older Docker installation)

4. **Initialize the database:**
```bash
# Wait for database to be ready (about 10 seconds)
sleep 10

# Initialize TimescaleDB extension
docker compose exec backend python scripts/init_db.py

# Run migrations
docker compose exec backend alembic upgrade head

# Seed sample data (optional)
docker compose exec backend python scripts/seed_data.py
```

5. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Local Development Setup

### Backend

1. **Create virtual environment (Python 3.11 recommended):**
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL:**
   - Install PostgreSQL 15+ with TimescaleDB extension
   - Create database: `createdb horizon`
   - Create user: `createuser -P horizon` (password: horizon)

4. **Initialize database:**
```bash
# Initialize TimescaleDB extension
python scripts/init_db.py

# Generate initial migration (first time only)
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head

# Seed sample data
python scripts/seed_data.py
```

5. **Run the server:**
```bash
uvicorn app.main:app --reload
```

### Frontend

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Running ETL Flows

To ingest data from public sources:

```bash
cd backend
python -m app.etl.flows
```

Or with Prefect Cloud/Server:

```bash
prefect deploy app/etl/flows.py:ingest_public_data_flow
prefect deploy app/etl/flows.py:ingest_synthetic_data_flow
```

## Troubleshooting

### Database Connection Issues

If you see connection errors:
1. Ensure PostgreSQL is running
2. Check DATABASE_URL in `.env` file
3. Verify TimescaleDB extension is installed: `psql -U horizon -d horizon -c "SELECT * FROM pg_extension WHERE extname = 'timescaledb';"`

### Frontend Not Connecting to Backend

1. Check that backend is running on port 8000
2. Verify CORS settings in `backend/app/core/config.py`
3. Check browser console for errors

### Migration Issues

If migrations fail:
1. Ensure database is initialized with TimescaleDB extension
2. Check Alembic version table: `SELECT * FROM alembic_version;`
3. Try: `alembic stamp head` to mark current state

## Next Steps

1. Configure OpenRouter API key for LLM features
2. Set up MLflow tracking server (optional)
3. Configure Snowflake connection (optional, for analytics warehouse)
4. Set up Prefect Cloud/Server for production ETL scheduling

## Production Deployment

For production deployment:
1. Change SECRET_KEY in `.env`
2. Use environment-specific database credentials
3. Set up proper CORS origins
4. Configure SSL/TLS certificates
5. Set up monitoring and logging
6. Configure backup strategy for PostgreSQL

