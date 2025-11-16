# Deploying Horizon to Render

Render supports native deployments without Docker. This guide captures the **step‑by‑step instructions** to deploy the current Horizon app (backend + frontend + database) to Render.

---

## Quick Start Checklist

1. **Fork/Connect repo** to Render (GitHub/GitLab).
2. **Create PostgreSQL DB** in Render, enable `timescaledb` extension.
3. **Create backend web service** (`horizon-backend`) using Python environment.
4. **Create frontend static site** (`horizon-frontend`) using the Vite build.
5. **Set environment variables**:
   - Backend: `DATABASE_URL`, `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `SECRET_KEY`, `CORS_ORIGINS`.
   - Frontend: `VITE_API_URL` pointing to the backend `/api` URL.
6. **Run migrations** (`alembic upgrade head`) from the backend Shell on first deploy.
7. (Optional) **Seed or ingest data** using the scripts in `backend/scripts/` (e.g., `fetch_real_data.py`, `ingest_local_datasets.py`).

---

## Overview

You'll deploy:
1. **Backend** - As a Web Service (Python)
2. **Frontend** - As a Static Site (or Web Service with Node)
3. **Database** - Managed PostgreSQL (with TimescaleDB extension)

## Step 1: Set Up PostgreSQL Database

1. In Render Dashboard, create a **PostgreSQL** database
2. Note the **Internal Database URL** (for backend)
3. Note the **External Database URL** (for local access if needed)
4. After creation, go to the database's **Shell** tab and run:
   ```sql
   CREATE EXTENSION IF NOT EXISTS timescaledb;
   ```

## Step 2: Deploy Backend

1. **Create a new Web Service** in Render
2. **Connect your repository** (GitHub/GitLab)
3. **Configure:**
   - **Name**: `horizon-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

4. **Environment Variables:**
   ```
   DATABASE_URL=<Internal Database URL from Step 1>
   OPENROUTER_API_KEY=<your-key-here>
   OPENROUTER_MODEL=openai/gpt-4o-mini
   SECRET_KEY=<generate-a-random-secret-key>
   CORS_ORIGINS=https://your-frontend-url.onrender.com
   ```

5. **Deploy** - Render will automatically build and deploy

## Step 3: Deploy Frontend

### Option A: Static Site (Recommended)

1. **Create a new Static Site** in Render
2. **Configure:**
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Root Directory**: `frontend`

3. **Environment Variables:**
   ```
   VITE_API_URL=https://horizon-backend.onrender.com/api
   ```

4. Render will automatically deploy your frontend

### Option B: Web Service (If you need SSR)

1. **Create a new Web Service** (Node)
2. **Build Command**: `cd frontend && npm install && npm run build`
3. **Start Command**: `cd frontend && npm run preview` (or use a simple Node server)
4. **Root Directory**: `frontend`

## Step 4: Run Database Migrations

After backend is deployed, run migrations:

1. Go to your backend service in Render
2. Open the **Shell** tab
3. Run:
   ```bash
   alembic upgrade head
   ```

Or add a one-time script that runs migrations on deploy (see below).

## Step 5: Seed Initial Data (Optional)

In the backend Shell:
```bash
python scripts/seed_data.py
```

## Render Configuration Files

Create these files to help Render deploy correctly:

### `render.yaml` (Optional - for Infrastructure as Code)

```yaml
services:
  - type: web
    name: horizon-backend
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: horizon-db
          property: connectionString
      - key: OPENROUTER_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: CORS_ORIGINS
        value: https://horizon-frontend.onrender.com

  - type: web
    name: horizon-frontend
    env: static
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    envVars:
      - key: VITE_API_URL
        value: https://horizon-backend.onrender.com/api

databases:
  - name: horizon-db
    databaseName: horizon
    user: horizon
    plan: free
```

## Post-Deploy Script (for migrations)

Create `backend/render-build.sh`:

```bash
#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed data (optional, only on first deploy)
# python scripts/seed_data.py
```

Then update Render's **Build Command** to:
```bash
cd backend && chmod +x render-build.sh && ./render-build.sh
```

## Environment Variables Reference

### Backend
- `DATABASE_URL` - Auto-provided by Render (Internal Database URL)
- `OPENROUTER_API_KEY` - Your OpenRouter API key
- `OPENROUTER_MODEL` - Model to use (default: `openai/gpt-4o-mini`)
- `SECRET_KEY` - Random secret for JWT (generate with: `openssl rand -hex 32`)
- `CORS_ORIGINS` - Frontend URL(s), comma-separated
- `PORT` - Auto-set by Render (don't override)

### Frontend
- `VITE_API_URL` - Backend API URL

## Important Notes

1. **Database URL**: Use the **Internal Database URL** in backend (not external)
2. **CORS**: Update `CORS_ORIGINS` to include your frontend URL
3. **Port**: Render sets `$PORT` automatically - use it in start command
4. **TimescaleDB**: Must be enabled manually via database Shell
5. **Migrations**: Run manually first time, then automate with build script

## Troubleshooting

### Backend won't start
- Check logs in Render dashboard
- Verify `DATABASE_URL` is set correctly
- Ensure `PORT` environment variable is used in start command

### Database connection errors
- Use Internal Database URL (not External)
- Verify TimescaleDB extension is installed
- Check database is running

### Frontend can't reach backend
- Update `VITE_API_URL` to backend URL
- Check CORS settings in backend
- Verify backend is deployed and running

### Migrations fail
- Run manually in Shell first
- Check database URL is correct
- Verify Alembic is in requirements.txt

## Cost Estimate (Free Tier)

- **Backend Web Service**: Free (with limitations)
- **Frontend Static Site**: Free
- **PostgreSQL Database**: Free (limited to 90 days, then $7/month)

## Upgrading from Free Tier

For production:
- Upgrade database to paid plan ($7/month)
- Consider upgrading backend for better performance
- Set up custom domains
- Enable auto-deploy from main branch

