# Horizon Hackathon Guide

## Executive Summary

**Recommendation: Use Real Data with Mock Data Backup**

For your hackathon presentation, we recommend using **real data from public APIs** (OWID + Google Trends) as your primary data source, with **mock data as a reliable backup**. This approach:

- ✅ **Demonstrates real-world capability** - Shows the platform works with actual public health data
- ✅ **More impressive to judges** - Real data integration is a key differentiator
- ✅ **Reliable fallback** - Mock data ensures your demo works even if APIs are slow/down
- ✅ **Shows production readiness** - Real data pipelines demonstrate scalability

---

## Data Strategy for Hackathon

### Option 1: Real Data (Recommended for Demo)

**Use when:**
- You want to impress judges with real-world data integration
- APIs are accessible and responsive
- You have time to run data ingestion before presentation

**How to set up:**
```bash
# 1. Run real data ingestion
cd backend
source venv/bin/activate
python scripts/fetch_real_data.py

# 2. Optionally ingest local CSV datasets
export LOCAL_DATASETS_DIR="/Users/tylin/Desktop/datasets"
python scripts/ingest_local_datasets.py
```

**What this gives you:**
- Real COVID-19 metrics from Our World in Data (OWID)
- Live Google Trends symptom search data for all US states
- Risk scores calculated from actual epidemiological trends
- Hospital utilization data from local CSV files

**Pros:**
- ✅ Authentic, real-world data
- ✅ Impressive to judges
- ✅ Shows production readiness
- ✅ Demonstrates API integration capabilities

**Cons:**
- ⚠️ Requires internet connection
- ⚠️ Google Trends API can be rate-limited
- ⚠️ May take 2-5 minutes to fetch all data

### Option 2: Mock Data (Reliable Backup)

**Use when:**
- APIs are slow or unavailable
- You need instant demo setup
- You want predictable, consistent data for presentation

**How to set up:**
```bash
cd backend
source venv/bin/activate
python scripts/seed_data.py
```

**What this gives you:**
- Sample risk scores for 5 regions (US-CA, US-NY, US-TX, US-FL, US-IL)
- Mock search trends, pharmacy data, hospital utilization
- Sample alerts and fund allocations
- Consistent, predictable data

**Pros:**
- ✅ Fast and reliable
- ✅ No external dependencies
- ✅ Consistent demo experience
- ✅ Works offline

**Cons:**
- ⚠️ Less impressive than real data
- ⚠️ Doesn't demonstrate API integration

### Option 3: Hybrid Approach (Best for Hackathon)

**Recommended workflow:**

1. **Before presentation (30 minutes prior):**
   ```bash
   # Try to fetch real data
   python scripts/fetch_real_data.py
   
   # If that fails or is slow, fall back to mock data
   python scripts/seed_data.py
   ```

2. **During presentation:**
   - If you have real data: Highlight the real-world integration
   - If using mock data: Explain it's "production-ready with real API integration" (which is true)

3. **Show both capabilities:**
   - Mention that the platform supports both real-time API data and batch CSV ingestion
   - Point to the ETL flows as evidence of production readiness

---

## Local Development Setup

### Quick Start (No Docker)

**1. Prerequisites:**
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# If not running:
brew services start postgresql@15
```

**2. Backend Setup:**
```bash
cd backend

# Create virtual environment (if not exists)
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb horizon  # if not exists
psql horizon -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# Run migrations
alembic upgrade head

# Load data (choose one):
# Option A: Real data
python scripts/fetch_real_data.py

# Option B: Mock data
python scripts/seed_data.py

# Option C: Both (real + local CSVs)
python scripts/fetch_real_data.py
export LOCAL_DATASETS_DIR="/Users/tylin/Desktop/datasets"
python scripts/ingest_local_datasets.py

# Start backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**3. Frontend Setup:**
```bash
cd frontend

# Install dependencies (if not done)
npm install

# Start development server
npm run dev
```

**4. Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Using Docker (Alternative)

```bash
# Start all services
docker compose up -d

# Wait for database
sleep 10

# Run migrations
docker compose exec backend alembic upgrade head

# Seed data
docker compose exec backend python scripts/seed_data.py

# Or fetch real data
docker compose exec backend python scripts/fetch_real_data.py
```

---

## Deployment Configuration

### Render Deployment (Recommended for Hackathon)

Render is perfect for hackathons because:
- ✅ Free tier available
- ✅ Easy setup (no Docker needed)
- ✅ Automatic HTTPS
- ✅ Fast deployment

**Step-by-step:**

1. **Create PostgreSQL Database:**
   - In Render Dashboard → New → PostgreSQL
   - Name: `horizon-db`
   - Plan: Free (or Starter for production)
   - After creation, go to Shell and run:
     ```sql
     CREATE EXTENSION IF NOT EXISTS timescaledb;
     ```

2. **Deploy Backend:**
   - New → Web Service
   - Connect your GitHub repo
   - Settings:
     - **Name**: `horizon-backend`
     - **Environment**: Python 3
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     ```
     DATABASE_URL=<Internal Database URL from PostgreSQL>
     OPENROUTER_API_KEY=<your-key>
     OPENROUTER_MODEL=openai/gpt-4o-mini
     SECRET_KEY=<generate-random-key>
     CORS_ORIGINS=https://horizon-frontend.onrender.com
     ```

3. **Deploy Frontend:**
   - New → Static Site
   - Connect your GitHub repo
   - Settings:
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `frontend/dist`
   - Environment Variables:
     ```
     VITE_API_URL=https://horizon-backend.onrender.com/api
     ```

4. **Run Migrations:**
   - Go to backend service → Shell
   - Run: `alembic upgrade head`

5. **Load Data:**
   - In backend Shell:
     ```bash
     # Real data
     python scripts/fetch_real_data.py
     
     # Or mock data
     python scripts/seed_data.py
     ```

### Environment Variables Reference

**Backend (.env or Render env vars):**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/horizon
OPENROUTER_API_KEY=your-api-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
SECRET_KEY=generate-random-secret-key
CORS_ORIGINS=http://localhost:3000,https://your-frontend-url.onrender.com
```

**Frontend (Render env vars):**
```bash
VITE_API_URL=https://horizon-backend.onrender.com/api
```

---

## Presentation Tips

### What to Highlight

1. **Real Data Integration:**
   - "Our platform integrates with real public health APIs"
   - Show OWID data source
   - Mention Google Trends integration

2. **AI/ML Capabilities:**
   - Risk scoring algorithm
   - Anomaly detection
   - AI-powered chat assistant (Horizon Assistant)

3. **Production-Ready Architecture:**
   - ETL pipelines (Prefect)
   - Time-series database (TimescaleDB)
   - Multi-tenant support
   - RESTful API design

4. **User Experience:**
   - Clean, modern UI
   - Real-time dashboards
   - Interactive risk maps
   - Alert system

### Demo Flow (5-10 minutes)

1. **Introduction (1 min):**
   - "Horizon is an AI-powered outbreak detection platform"
   - "We integrate real-time data from multiple sources"

2. **Dashboard Overview (2 min):**
   - Show risk scores by region
   - Highlight real data sources
   - Show trend charts

3. **Risk Map (1 min):**
   - Visual representation of outbreak risks
   - Explain color coding

4. **Alerts System (1 min):**
   - Show high-risk alerts
   - Demonstrate alert acknowledgment

5. **AI Assistant (2 min):**
   - Ask: "Why did Region X's risk increase?"
   - Show natural language explanations
   - Highlight AI reasoning capabilities

6. **Technical Deep Dive (2 min):**
   - Show API documentation (http://localhost:8000/docs)
   - Mention ETL pipelines
   - Highlight scalability features

### Backup Plan

If something goes wrong during demo:

1. **API fails:** Switch to mock data (already seeded)
2. **Database issues:** Use pre-seeded data
3. **Frontend won't load:** Show API docs and backend directly
4. **Internet issues:** Use localhost demo with mock data

---

## Pre-Presentation Checklist

### 30 Minutes Before

- [ ] Backend is running and accessible
- [ ] Frontend is running and connects to backend
- [ ] Database has data (real or mock)
- [ ] Test all major features:
  - [ ] Dashboard loads
  - [ ] Risk scores display
  - [ ] Charts render
  - [ ] AI Assistant responds
  - [ ] Alerts show correctly
- [ ] OpenRouter API key is configured (for AI features)
- [ ] Take screenshots as backup

### 10 Minutes Before

- [ ] Refresh browser to ensure latest data
- [ ] Test AI Assistant with a sample question
- [ ] Verify all charts are rendering
- [ ] Check API docs are accessible

### During Presentation

- [ ] Have backup screenshots ready
- [ ] Keep terminal open to restart services if needed
- [ ] Have mock data script ready to run if APIs fail

---

## Troubleshooting

### Backend won't start
```bash
# Check database connection
psql horizon -c "SELECT 1;"

# Check environment variables
cd backend
source venv/bin/activate
python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

### Frontend can't connect to backend
- Check `VITE_API_URL` in frontend
- Verify backend is running on port 8000
- Check CORS settings in backend config

### No data showing
```bash
# Check database has data
psql horizon -c "SELECT COUNT(*) FROM risk_scores;"

# If empty, seed data
cd backend
source venv/bin/activate
python scripts/seed_data.py
```

### Google Trends API fails
- This is common - use mock data instead
- Or reduce number of regions in fetch_real_data.py

### OpenRouter API fails
- AI Assistant will still work, just slower
- Or use mock responses for demo

---

## Quick Reference Commands

```bash
# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Start frontend
cd frontend && npm run dev

# Fetch real data
cd backend && source venv/bin/activate && python scripts/fetch_real_data.py

# Seed mock data
cd backend && source venv/bin/activate && python scripts/seed_data.py

# Run migrations
cd backend && source venv/bin/activate && alembic upgrade head

# Check database
psql horizon -c "SELECT COUNT(*) FROM risk_scores;"
```

---

## Final Recommendation

**For Hackathon Presentation:**

1. **Primary:** Use real data (OWID + Google Trends) - shows real-world integration
2. **Backup:** Have mock data seeded and ready
3. **Deployment:** Use Render for easy, free hosting
4. **Demo:** Focus on AI capabilities and real data integration
5. **Backup Plan:** Screenshots and mock data ready if APIs fail

**Key Message:** "Horizon integrates real-time public health data with AI-powered risk assessment to provide early outbreak detection and actionable insights."

Good luck with your hackathon! 🚀

