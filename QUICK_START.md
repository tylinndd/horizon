# Quick Start Guide - Horizon

## Starting the Application

### 1. Start PostgreSQL (if not already running)
```bash
brew services start postgresql@15
```

### 2. Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Start Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Stopping Servers

```bash
# Stop backend
pkill -f uvicorn

# Stop frontend
pkill -f vite
```

## Database

- **Database Name**: horizon
- **User**: stephensookra (your macOS username)
- **Port**: 5432
- **Connection**: PostgreSQL is running via Homebrew service

## Environment Variables

Backend `.env` file is located at `backend/.env`:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENROUTER_API_KEY` - Optional, for LLM features
- `SECRET_KEY` - Secret key for JWT (change in production)
- `CORS_ORIGINS` - Allowed frontend origins

## First Time Setup (if starting fresh)

```bash
# Create database
createdb horizon

# Run migrations
cd backend
source venv/bin/activate
alembic upgrade head

# Seed sample data (optional)
python scripts/seed_data.py
```

## Troubleshooting

- **Port already in use**: Change port in uvicorn command or kill existing process
- **Database connection error**: Check PostgreSQL is running: `brew services list`
- **Module not found**: Make sure virtual environment is activated

