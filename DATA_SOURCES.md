## Horizon Data Sources

This document describes how Horizon can obtain the data it needs, where to find initial datasets, and **how to integrate each source into the app** using the existing tech stack (Postgres/TimescaleDB, Snowflake, Airflow/Prefect, and Python).

Horizon will combine:

- **Public / open datasets** (for MVP, research, baselines)
- **3rd‑party APIs** (e.g., Google Trends)
- **Customer / private data** from hospitals and companies

---

## 1. Public / Open Datasets

Use these to bootstrap models and demos before you have hospital partners. All of them can be ingested via scheduled ETL jobs (Airflow/Prefect) that download CSV/JSON and load into Postgres/TimescaleDB and Snowflake.

### 1.1 Our World in Data (OWID)

- **What it provides**
  - Global and country-level indicators: cases, hospitalizations, ICU usage, tests, vaccinations, etc.
- **Where to get it**
  - Website: [Our World in Data](https://ourworldindata.org/coronavirus)
  - Direct CSV (example): [`https://covid.ourworldindata.org/data/owid-covid-data.csv`](https://covid.ourworldindata.org/data/owid-covid-data.csv)
- **How to add it to Horizon**
  1. **Define a table** in Postgres/TimescaleDB, e.g. `owid_covid_metrics` with fields like:
     - `location`, `date`, `new_cases`, `new_deaths`, `hosp_patients`, `icu_patients`, `tests_per_thousand`, etc.
  2. **Create an ETL flow** (Airflow/Prefect):
     - Download the CSV to a staging location (local or object storage).
     - Load into Pandas, select and rename columns.
     - Upsert into `owid_covid_metrics` (and optionally copy to Snowflake).
  3. **Use in models** as a global baseline for:
     - Outbreak risk in regions.
     - Validation of your own signals versus official data.

### 1.2 WHO Data

- **What it provides**
  - Global and regional surveillance data for infectious diseases, including case counts and some hospitalization metrics.
- **Where to get it**
  - Portal: [WHO Data](https://www.who.int/data)
  - Example COVID-19 dataset: [WHO COVID-19 Global Data](https://covid19.who.int/data)
- **How to add it to Horizon**
  1. Identify CSV/JSON endpoints for:
     - Case counts by country/region and date.
  2. Build an ETL job that:
     - Downloads the dataset regularly (e.g., daily).
     - Normalizes region codes to match your internal `region_id` standard.
     - Loads into a table like `who_case_counts`.
  3. Use this table to:
     - Cross-check your model outputs.
     - Provide “ground truth” labels where possible.

### 1.3 CDC (US) – FluView / ILINet and other surveillance data

- **What it provides**
  - US influenza-like illness (ILI) indicators, lab-confirmed tests, and other surveillance metrics by region and time.
- **Where to get it**
  - CDC Data Portal: [CDC data](https://data.cdc.gov/)
  - Example searches:
    - “Influenza-Like Illness (ILI)”  
    - “FluView”  
  - Many datasets have APIs via Socrata, e.g.:  
    [`https://data.cdc.gov/resource/<dataset_id>.json`](https://data.cdc.gov/)
- **How to add it to Horizon**
  1. Choose 1–2 key datasets (e.g., ILI percentages by region and week).
  2. Use the Socrata API from Python:
     - Call the API with `requests`/`httpx`.
     - Parse JSON and convert to a normalized schema (e.g., `region`, `week_start`, `ili_percent`).
  3. Load into tables like `cdc_ili_metrics` and `cdc_lab_confirmed`.
  4. Integrate as features in your outbreak models, especially for US-focused deployments.

### 1.4 Hospital Utilization – US HealthData.gov

- **What it provides**
  - US hospital capacity and utilization: number of beds, ICU usage, occupancy, etc.
- **Where to get it**
  - Portal: [HealthData.gov](https://healthdata.gov/)
  - Search for “hospital utilization”, “bed occupancy”, “hospital capacity”.
- **How to add it to Horizon**
  1. Identify datasets with:
     - Facility/region identifiers.
     - Date, total beds, occupied beds, ICU metrics.
  2. Create an ETL job that:
     - Downloads CSV or uses the API.
     - Maps facility/region IDs to your internal `region_id`.
     - Loads into a table like `hospital_utilization_metrics`.
  3. Use as:
     - Features for risk models.
     - Benchmark data for pilot hospitals (e.g., compare their utilization to national averages).

### 1.5 Mobility / Contextual Data (Optional)

- **What it provides**
  - Mobility patterns, which can be useful features for transmission risk models.
- **Example sources**
  - Historical Google mobility reports: [Google Mobility Reports](https://www.google.com/covid19/mobility/) (static historical data).
  - Weather APIs: [Open-Meteo](https://open-meteo.com/) for temperature, humidity, etc.
- **How to add it to Horizon**
  1. For mobility CSVs:
     - Download and map regions to your `region_id`.
     - Load into `mobility_metrics` table.
  2. For weather:
     - Call the API periodically with `httpx`/`requests`.
     - Store daily weather summaries per region in `weather_metrics`.
  3. Incorporate into models as optional features.

---

## 2. 3rd‑Party APIs (Live Signals)

### 2.1 Google Trends (Symptom Search)

- **What it provides**
  - Relative search interest for symptom-related keywords by time and region.
- **Where to get it**
  - Google Trends web interface and unofficial libraries.
  - Common Python helper: [`pytrends`](https://github.com/GeneralMills/pytrends)
- **How to add it to Horizon**
  1. Define a list of symptom-related queries, e.g.:
     - “fever”, “cough”, “flu symptoms”, “shortness of breath”, etc.
  2. Use `pytrends` (or direct HTTP calls) in an **ETL flow (Airflow/Prefect)**:
     - Pull time-series interest for each query and region at regular intervals (e.g., every 1–4 hours).
  3. Load into a table like `search_trends_metrics`:
     - Columns: `tenant_id` (if relevant), `region_id`, `timestamp`, `keyword`, `search_index`.
  4. Use as an early indicator feature in your anomaly detection and risk models.

---

## 3. Customer / Private Data (Hospitals, Companies)

Once you have pilot partners, this becomes the **most valuable** part of your data pipeline. You will define schemas and ingestion patterns that fit Horizon’s models while staying within privacy and compliance constraints.

### 3.1 Pharmacy / Medication Aggregates

- **What it provides**
  - Aggregated counts of medication purchases or prescriptions by time, region, and category (no raw patient-level data).
- **How to get it**
  - Integration patterns:
    - **Batch files**: CSV/Parquet via SFTP or secure object storage.
    - **APIs**: Partner exposes a REST/FHIR endpoint that returns aggregated counts.
    - **Streams (later)**: Kafka/Pub/Sub topics with aggregated events.
- **How to add it to Horizon**
  1. Define a standard schema, e.g. `pharmacy_aggregates`:
     - `tenant_id`, `region_id`, `timestamp`, `drug_category`, `count`.
  2. For batch files:
     - Build an ETL flow that:
       - Watches a secure location (SFTP or bucket) for new files.
       - Validates schema and data types.
       - Loads into `pharmacy_aggregates` (and optionally Snowflake for analytics).
  3. For APIs:
     - Implement ingestion microservices in FastAPI that:
       - Authenticate the partner.
       - Accept POSTed JSON in your schema.
       - Write directly to Postgres/TimescaleDB.
  4. Use these aggregates as primary early signals in your outbreak models.

### 3.2 Hospital Supply & Utilization

- **What it provides**
  - Daily or hourly aggregates of:
    - Bed occupancy (general, ICU).
    - PPE usage and inventory levels.
    - Ventilator usage.
    - ER visit counts.
- **How to get it**
  - Similar integration patterns:
    - Batch CSV/Parquet exports.
    - Internal APIs or FHIR-based endpoints.
    - Event streams for more advanced partners.
- **How to add it to Horizon**
  1. Define tables like `hospital_supply_metrics` and `hospital_utilization_metrics` with:
     - `tenant_id`, `facility_id` or `region_id`, `timestamp`, `metric_type`, `value`.
  2. Build ETL/ingestion pipelines that:
     - Validate and transform partner data into this schema.
     - Handle id mapping (e.g., partner facility IDs → your standardized `facility_id` / `region_id`).
  3. Feed these metrics into:
     - Anomaly detection (e.g., sudden spikes in PPE usage).
     - Outbreak risk scoring models.

### 3.3 Insurer / Company-Level Indicators

- **What it provides**
  - Aggregated claims, sick leave, or other HR/insurance indicators for companies.
- **How to get it**
  - Data-sharing agreements with insurers or large employers.
  - Batch or API integrations with aggregates per company/region/time.
- **How to add it to Horizon**
  1. Define a schema like `company_health_signals`:
     - `tenant_id`, `company_id`, `region_id`, `timestamp`, `signal_type`, `value`.
  2. Ingest via:
     - ETL pipelines for CSV/Parquet.
     - FastAPI endpoints for direct push from partner systems.
  3. Use to generate:
     - Company-specific insights and risk dashboards.
     - Customized FinTech simulations (e.g., cost savings, risk-adjusted funding).

---

## 4. Synthetic / Simulated Data (When Real Data Is Missing)

- **Why use it**
  - To test your pipeline, dashboards, and models before you have real partner feeds.
- **How to add it to Horizon**
  1. Write Python scripts that:
     - Generate realistic time-series data for pharmacy, hospital usage, and company indicators.
     - Introduce synthetic “outbreaks” (spikes) in certain regions and time periods.
  2. Load the generated data into the same tables you will use for real data:
     - `pharmacy_aggregates`, `hospital_utilization_metrics`, `company_health_signals`, etc.
  3. Use this to:
     - Validate end-to-end flows (ingestion → ML → dashboards → FinTech simulations).
     - Demo Horizon’s capabilities to stakeholders.

---

## 5. Implementation Checklist

To integrate these datasets into Horizon in a concrete way:

- **Step 1: Create schemas**
  - Design Postgres/TimescaleDB tables for:
    - Public data (`owid_covid_metrics`, `who_case_counts`, `cdc_ili_metrics`, `hospital_utilization_metrics`, `search_trends_metrics`).
    - Partner data (`pharmacy_aggregates`, `hospital_supply_metrics`, `company_health_signals`).

- **Step 2: Build ETL flows**
  - Use Airflow or Prefect to:
    - Download public CSV/JSON/API data on schedules.
    - Validate, normalize, and load into Postgres/TimescaleDB and Snowflake.

- **Step 3: Wire into ML**
  - Use Python (Pandas, SQLAlchemy, Snowflake connector) to:
    - Pull training data from Postgres/Snowflake.
    - Construct features for outbreak and anomaly models.

- **Step 4: Connect dashboards**
  - Expose aggregated metrics and risk scores via FastAPI endpoints.
  - Visualize in the React dashboard and internal tools (Streamlit).

This approach lets you start immediately with **open data + synthetic data**, then smoothly plug in **real hospital/company feeds** as you sign partners, without changing your core architecture. 


