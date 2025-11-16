## Horizon Data Ingestion via Public APIs

This document summarizes **how to pull real data into Horizon** using the public APIs and libraries that are already reflected in the codebase.

The core idea: **your FastAPI backend always reads from Postgres tables** (e.g., `RiskScore`, `SearchTrend`, `PharmacyAggregate`, `HospitalUtilization`, `OWIDCovidMetric`). What makes the data “real” or “synthetic” is **which ETL jobs populate those tables**.

---

## 1. Our World in Data (OWID) – Real Epidemiological Metrics

- **Purpose**: Global and national COVID (and other disease) metrics: cases, deaths, hospital/ICU, testing.
- **Used for**:
  - Baseline outbreak severity.
  - Calibrating Horizon risk scores.
  - Historical trends for model training.
- **Endpoint pattern**:
  - CSV: `https://covid.ourworldindata.org/data/owid-covid-data.csv`

### 1.1 How Horizon uses OWID today

- Code: `app/etl/flows.py` (`fetch_owid_covid_data`, `load_owid_data_to_db`)
- Script: `scripts/fetch_real_data.py`
- Flow:
  1. Download OWID CSV with `pandas.read_csv(url)`.
  2. Filter to recent rows (e.g., last 30–90 days).
  3. Map columns into `OWIDCovidMetric` ORM model.
  4. `db.merge(...)` rows into Postgres.

You can trigger the Prefect flow directly:

```bash
cd backend
source venv/bin/activate
python -c "from app.etl.flows import ingest_public_data_flow; ingest_public_data_flow()"
```

Or run the real-data script:

```bash
cd backend
source venv/bin/activate
python scripts/fetch_real_data.py
```

---

## 2. Google Trends – Live Symptom Search Signals (via `pytrends`)

- **Purpose**: Leading indicator of outbreaks based on symptom search volume.
- **Used for**:
  - Early warning signals per region.
  - Features for risk scoring and anomaly detection.
- **Access method**:
  - Library: `pytrends` (already in `backend/requirements.txt`).
  - No API key required; `pytrends` simulates browser requests.

### 2.1 Regions and keywords

You can reuse the existing region codes and keywords:

- Regions (geo codes): `US-CA`, `US-NY`, `US-TX`, `US-FL`, `US-IL`
- Example keywords:
  - `fever`
  - `cough`
  - `flu symptoms`
  - `shortness of breath`

### 2.2 How Horizon uses Google Trends

- Code:
  - Prefect task: `fetch_google_trends` in `app/etl/flows.py`
  - Real-data script: `update_search_trends` in `scripts/fetch_real_data.py`
- Flow:
  1. Create a `TrendReq` client from `pytrends.request`.
  2. For each region, call `build_payload` with a list of symptom keywords and a timeframe (e.g., last 7 days).
  3. Call `interest_over_time()` to get a `DataFrame` per region.
  4. For each (region, keyword, timestamp) row, write an entry into `SearchTrend`.

Once these jobs are scheduled, your `/health/search-trends` and risk-scoring logic will automatically use **live Google Trends data**.

---

## 3. CDC & HealthData.gov – US Surveillance and Hospital Capacity

These are **not yet fully wired into code**, but the patterns are straightforward and match existing ETL flows.

### 3.1 CDC (FluView / ILINet and others)

- **Purpose**: Seasonal influenza and respiratory surveillance in the US.
- **Where**:
  - Portal: `https://data.cdc.gov/`
  - Many datasets expose a Socrata API:
    - Pattern: `https://data.cdc.gov/resource/<dataset_id>.json`
- **Recommended ETL pattern**:
  1. Use `requests` or `httpx` to call the JSON API on a schedule.
  2. Normalize fields into consistent schemas, e.g.:
     - `region`, `week_start`, `ili_percent`, `lab_confirmed_cases`
  3. Load into tables like `cdc_ili_metrics`, `cdc_lab_confirmed`.
  4. Use these features in ML pipelines (e.g., as seasonal baseline risk).

### 3.2 HealthData.gov – Hospital Utilization

- **Purpose**: Bed occupancy, ICU usage, ER visits, hospital capacity.
- **Where**:
  - Portal: `https://healthdata.gov/`
  - Search for “hospital utilization” / “hospital capacity”.
- **Recommended ETL pattern**:
  1. Identify CSV or API endpoints that include:
     - Facility/region ID
     - Date
     - Total beds / occupied beds / ICU usage metrics
  2. Use `pandas.read_csv()` or `requests.get()` to download data in your ETL job.
  3. Map into `HospitalUtilization` or a new table, e.g. `hospital_utilization_metrics`:
     - `tenant_id`, `region_id` / `facility_id`, `timestamp`, `metric_type`, `value`, `unit`.

Once wired, these can directly feed:

- `/health/hospital-utilization` FastAPI endpoint.
- Risk scoring via `hospital_utilization` features in the ML service.

---

## 4. Customer / Partner Data (Pharmacy, Hospitals, Insurers)

This is where Horizon becomes most valuable; it requires legal and technical integrations, but the ingestion pattern reuses all of the above.

### 4.1 Pharmacy / Medication Aggregates

- **Source**: Retail pharmacy chains, wholesalers, or local hospital pharmacies.
- **Data shape**:
  - `tenant_id`, `region_id`, `timestamp`, `drug_category`, `count`
- **Integration patterns**:
  - Scheduled CSV/Parquet drops (SFTP, secure bucket).
  - Partner REST/FHIR APIs with aggregated counts.

### 4.2 Hospital Supply & Utilization

- **Source**: Partner hospitals / health systems.
- **Data shape**:
  - `tenant_id`, `facility_id` or `region_id`, `timestamp`, `metric_type`, `value`, `unit`
- **Integration patterns**:
  - Nightly CSV exports.
  - Internal APIs or event streams (Kafka/Pub/Sub) for more advanced partners.

### 4.3 Insurer / Employer Health Indicators

- **Source**: Insurers or large employers.
- **Data shape**:
  - `tenant_id`, `company_id`, `region_id`, `timestamp`, `signal_type`, `value`
- **Integration patterns**:
  - Batch data sharing.
  - API-based push of aggregates.

---

## 5. How This Connects to the App

- **Backend**:
  - ETL jobs (Prefect flows and scripts under `backend/app/etl` and `backend/scripts`) populate Postgres tables.
  - FastAPI endpoints (e.g., `/risk/scores`, `/risk/scores/latest`, `/health/search-trends`, `/health/pharmacy`) read from those tables.
- **Frontend**:
  - Uses `frontend/src/services/api.ts` to call the backend APIs.
  - It is **agnostic** to whether data is simulated or real; once ETL flows use OWID, Google Trends, CDC, and partner feeds, the UI automatically reflects real-world signals.

To **fully move from synthetic to real data**, prioritize:

1. Ensure `scripts/fetch_real_data.py` and `app/etl/flows.py` are run regularly.
2. Stop relying on `scripts/update_realistic_data.py` and `scripts/seed_data.py` except for demos/tests.
3. Gradually add CDC/HealthData.gov and partner ETLs following the patterns above.


