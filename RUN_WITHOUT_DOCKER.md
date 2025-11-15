# Running Horizon Without Docker

If you don't have Docker installed, you can run the application components separately.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ with TimescaleDB extension

## Step 1: Set Up PostgreSQL

1. **Install PostgreSQL:**
   ```bash
   brew install postgresql@15
   brew install timescaledb
   ```

2. **Start PostgreSQL:**
   ```bash
   brew services start postgresql@15
   ```

3. **Create database:**
   ```bash
   createdb horizon
   psql horizon -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
   ```

## Step 2: Set Up Backend

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and set DATABASE_URL if different
   ```

5. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Seed sample data (optional):**
   ```bash
   python scripts/seed_data.py
   ```

7. **Start backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

Backend will be available at: http://localhost:8000

## Step 3: Set Up Frontend

1. **Open a new terminal and navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

Frontend will be available at: http://localhost:3000

## Running ETL Flows

In the backend directory with virtual environment activated:

```bash
python -m app.etl.flows
```

## Troubleshooting

### PostgreSQL Connection Issues

If you get connection errors:
- Check PostgreSQL is running: `brew services list`
- Verify database exists: `psql -l | grep horizon`
- Check TimescaleDB extension: `psql horizon -c "SELECT * FROM pg_extension WHERE extname = 'timescaledb';"`

### Port Conflicts

If ports 8000 or 3000 are already in use:
- Backend: Change port in `uvicorn app.main:app --port 8001 --reload`
- Frontend: Change port in `vite.config.ts` and update proxy settings

### Python Dependencies

If you encounter import errors:
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

