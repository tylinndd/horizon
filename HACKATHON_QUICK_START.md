# Horizon Hackathon Quick Start

## TL;DR - What You Need to Know

### Data Strategy: **Hybrid Approach** ✅

**Use real data (OWID + Google Trends) as primary, with mock data as backup.**

### Quick Setup (5 minutes)

```bash
# 1. Setup (first time only)
make setup

# 2. Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# 3. Start frontend (new terminal)
cd frontend && npm run dev

# 4. Prepare data (new terminal)
make hackathon-prep
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Why Hybrid Approach?

1. **Real Data** = Impressive to judges, shows production readiness
2. **Mock Data Backup** = Reliable demo, works even if APIs fail
3. **Best of Both** = Professional presentation with guaranteed reliability

---

## Pre-Presentation Checklist

### 30 Minutes Before
```bash
# Prepare data
make hackathon-prep

# Verify backend is running
curl http://localhost:8000/api/health/metrics

# Verify frontend loads
open http://localhost:3000
```

### 10 Minutes Before
- [ ] Refresh browser
- [ ] Test AI Assistant
- [ ] Verify charts render
- [ ] Check API docs accessible

---

## If Something Goes Wrong

### APIs Fail → Use Mock Data
```bash
cd backend && source venv/bin/activate
python scripts/seed_data.py
```

### Database Empty → Check Migrations
```bash
cd backend && source venv/bin/activate
alembic upgrade head
make hackathon-prep
```

### Frontend Won't Connect → Check CORS
- Verify `VITE_API_URL` in frontend
- Check backend is running on port 8000
- Check CORS settings in `backend/app/core/config.py`

---

## Deployment (Render)

### Backend
1. Create PostgreSQL database
2. Create Web Service (Python)
3. Set environment variables
4. Run migrations in Shell

### Frontend
1. Create Static Site
2. Set `VITE_API_URL` env var
3. Deploy

See `RENDER_DEPLOYMENT.md` for details.

---

## Key Talking Points

1. **Real Data Integration**: "We integrate live data from OWID and Google Trends"
2. **AI-Powered**: "Our ML models detect anomalies and assess outbreak risks"
3. **Production-Ready**: "ETL pipelines, time-series database, scalable architecture"
4. **User Experience**: "Clean UI, real-time dashboards, AI assistant"

---

## Full Documentation

See `HACKATHON_GUIDE.md` for complete details.

