## Horizon – Local Dev & Data Integration Notes

This file summarizes the key ideas and changes we made so you can reliably run Horizon **locally without Docker** and combine **multiple data sources** (APIs + CSVs) in one place.

---

## 1. How the app gets its data

- **Backend reads only from Postgres**, not directly from CSVs or APIs.
- Data arrives in the DB from:
  - **Public/real sources**:
    - OWID (Our World in Data) via `scripts/fetch_real_data.py`
    - Google Trends via `pytrends` in:
      - `app/etl/flows.py::fetch_google_trends`
      - `scripts/fetch_real_data.py::update_search_trends`
  - **Local CSV datasets**:
    - `backend/scripts/ingest_local_datasets.py` loads selected CSVs into `HospitalUtilization` and related tables.
  - **Synthetic data scripts** (for demos/testing):
    - `scripts/update_realistic_data.py`
    - `scripts/seed_data.py`

The frontend and APIs just reflect whatever is in tables like `risk_scores`, `search_trends_metrics`, and `hospital_utilization_metrics`.

---

## 2. Running the app without Docker

You can run everything locally (no containers) with:

```bash
cd /Users/tylin/horizon
make setup
```

Then:

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend (in another terminal)
cd /Users/tylin/horizon/frontend
npm run dev
```

Requirements:

- Local PostgreSQL 15+ running.
- `DATABASE_URL` either:
  - Uses the default `postgresql://horizon:horizon@localhost:5432/horizon` **and** you create that DB/user, or
  - Is overridden in `backend/.env` to something like `postgresql://$USER@localhost:5432/horizon`.

---

## 3. Local PostgreSQL + TimescaleDB

- Postgres 15 is installed via Homebrew (`brew install postgresql@15`).
- Binaries (including `createdb`, `psql`) live at:

```bash
/opt/homebrew/opt/postgresql@15/bin
```

- To make them available globally:

```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

- Key commands:

```bash
# Create DB (done once; ignore "already exists" warnings if rerun)
createdb horizon

# Connect to DB
psql horizon

# Check table counts (inside psql)
SELECT count(*) FROM risk_scores;
SELECT count(*) FROM search_trends_metrics;
SELECT count(*) FROM hospital_utilization_metrics;
```

> Note: TimescaleDB is optional for local dev. If the extension is not installed, you can skip `CREATE EXTENSION timescaledb;` and still run the app on plain Postgres.

---

## 4. Real data ingestion (APIs)

**One-shot refresh with real data**:

```bash
cd /Users/tylin/horizon
source backend/venv/bin/activate
make update-data
```

This runs `backend/scripts/fetch_real_data.py` which:

- Pulls real OWID COVID data into `OWIDCovidMetric`.
- Generates regional `risk_scores` based on recent OWID trends.
- Uses `pytrends` to pull symptom search data for all US states (and DC) into `search_trends_metrics`.

You can also run the Prefect flow directly:

```bash
cd /Users/tylin/horizon/backend
source venv/bin/activate
python -c "from app.etl.flows import ingest_public_data_flow; ingest_public_data_flow()"
```

---

## 5. Local CSV ingestion

Local datasets (e.g., from `/Users/tylin/Desktop/datasets`) are ingested with:

```bash
cd /Users/tylin/horizon
source backend/venv/bin/activate
export LOCAL_DATASETS_DIR="/Users/tylin/Desktop/datasets"
make ingest-local
```

`backend/scripts/ingest_local_datasets.py` currently supports:

- `hospital-utilization-trends.csv`  
  → stored as `HospitalUtilization` records with `metric_type` like `ambulatory_surgery_volume`.
- `four-quarter-summary-hospital-utilization-operating-revenue-and-profit-margins.csv`  
  → stored as `HospitalUtilization` records with `metric_type` `total_margin` and `operating_margin`.
- `monthly-share-of-influenza-tests-that-were-positive.csv`  
  → stored as `HospitalUtilization` records with `metric_type` `flu_test_positive_share`.

These are **additive** and do not replace data from OWID/Google Trends; they simply add more rows for the backend to use.

---

## 6. Horizon Assistant context wiring

The Horizon Assistant now gets live context from the dashboard:

- In `Dashboard.tsx`, we pass current `riskScores` and `alerts` into the assistant:

```tsx
<HorizonAssistant
  context={{
    riskScores,
    alerts,
  }}
/>
```

- In `HorizonAssistant.tsx`, we forward a compact snapshot of that context to the backend LLM via `queryLLM(query, contextPayload)`.

This allows the assistant to:

- Explain patterns in risk scores.
- Discuss possible outbreaks given current metrics.
- Give prevention suggestions and qualitative cost/impact guidance.

---

## 7. Running everything together (summary)

Typical workflow without Docker:

```bash
# 1) Setup (once)
cd /Users/tylin/horizon
make setup

# 2) Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 3) Frontend (new terminal)
cd /Users/tylin/horizon/frontend
npm run dev

# 4) Data ingestion (new terminal)
cd /Users/tylin/horizon
source backend/venv/bin/activate
make update-data
export LOCAL_DATASETS_DIR="/Users/tylin/Desktop/datasets"
make ingest-local
```

After these steps, the dashboard and assistant should reflect a combination of:

- Real public data (OWID + Google Trends),
- Local CSV-derived metrics,
- Any synthetic data you choose to keep using for demos.


