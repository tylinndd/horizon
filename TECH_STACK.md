## Horizon Tech Stack

This document describes the proposed production-ready tech stack for **Horizon**, including how each technology fits into the architecture, how it should be implemented, and the key libraries/frameworks to install.

Horizon is composed of the following layers:

- **Data & Ingestion Layer**
- **AI & Analytics Layer**
- **LLM / OpenRouter Reasoning Layer**
- **Backend API & Integration Layer**
- **Dashboard / Frontend Layer**
- **FinTech Simulation Layer**
- **Infrastructure, Security, and DevOps**

Each section below follows this structure:

- **What it does**
- **How it fits Horizon**
- **Implementation notes**
- **Key libraries / tools to install**

---

## Data & Ingestion Layer

This layer pulls raw signals (search trends, pharmacy data, hospital supply usage, public health indicators) and turns them into clean, time-series data that downstream systems can consume.

### PostgreSQL + TimescaleDB (Operational Store)

- **What it does**
  - Stores historical and real-time time-series data (per region, per organization).
  - Supports fast aggregations, rollups, and window queries for outbreak detection.

- **How it fits Horizon**
  - Central store for:
    - Pharmacy purchases by region / product.
    - Search trends by region / symptom.
    - Hospital supply usage (PPE, beds, ventilators).
    - Computed risk scores and anomaly flags.
  - Enables per-company and global analytics (multi-tenant).

- **Implementation notes**
  - Use **PostgreSQL** as the primary relational DB.
  - Add **TimescaleDB** extension for efficient time-series operations.
  - Design tables with:
    - `tenant_id` (organization), `region_id`, `timestamp`, metric columns.
    - Indices on `tenant_id`, `region_id`, `timestamp`.
  - Consider row-level security (RLS) to isolate tenant data.

- **Key libraries / tools**
  - Server: PostgreSQL + TimescaleDB
  - Python:
    - `psycopg2-binary` or `asyncpg`
    - `SQLAlchemy` (ORM)
    - `alembic` (migrations)

  ```bash
  pip install sqlalchemy psycopg2-binary alembic
  ```

### Analytics Warehouse: Snowflake

- **What it does**
  - Acts as a scalable cloud data warehouse for large analytical workloads.
  - Stores long-term, historical data across all tenants and regions.
  - Supports complex, cross-tenant analytics and BI without overloading the operational DB.

- **How it fits Horizon**
  - Holds:
    - Long-term history of health indicators (pharmacy, search, supplies).
    - Historical risk scores, alerts, and FinTech allocations.
  - Used for:
    - Deep analytics and executive reporting (via BI tools).
    - Building large training datasets for ML models.
    - Cross-tenant, anonymized benchmarking and research.

- **Implementation notes**
  - Keep **Postgres/TimescaleDB** as the primary operational store for “hot” data and the application backend.
  - Use **Snowflake** as the analytical warehouse:
    - Periodically copy data from Postgres/TimescaleDB and raw files (CSV/Parquet in S3/GCS) into Snowflake.
    - Build cleaned, denormalized tables and views optimized for analytics and model training.
  - Implement ETL/ELT flows (via Airflow/Prefect and/or dbt) that:
    - Extract data from Postgres and object storage.
    - Load into Snowflake staging tables.
    - Transform into curated schemas for analytics and ML.
  - Connect BI tools (e.g., Tableau/Power BI/Metabase) and ML workflows to Snowflake instead of hitting the operational DB directly for heavy queries.

- **Key libraries / tools**
  - Snowflake account and warehouse.
  - Python:

  ```bash
  pip install snowflake-connector-python
  pip install "apache-airflow-providers-snowflake"  # if using Airflow
  pip install dbt-snowflake                         # optional, for dbt
  ```

### Batch Ingestion: Airflow or Prefect

- **What it does**
  - Orchestrates scheduled jobs that periodically pull data (e.g., every 1–5 minutes).
  - Manages dependencies, retries, and monitoring of ETL tasks.

- **How it fits Horizon**
  - Runs periodic pipelines to:
    - Pull Google Trends and other public APIs.
    - Ingest CSV/SFTP uploads from hospitals and companies.
    - Normalize and load into Postgres/TimescaleDB.

- **Implementation notes**
  - Choose **Prefect** (simpler to start) or **Apache Airflow** (more enterprise-standard).
  - Define flows/DAGs for:
    - `fetch_google_trends`
    - `ingest_pharmacy_data`
    - `ingest_hospital_supply_usage`
    - `compute_aggregated_features`
  - Run flows at 1–5 minute intervals for “near real-time” updates.

- **Key libraries / tools**
  - Prefect:

    ```bash
    pip install prefect
    ```

  - Airflow (alternative):

    ```bash
    pip install apache-airflow
    ```

### Optional Streaming: Kafka / Cloud Pub/Sub

- **What it does**
  - Provides a high-throughput message bus for real-time event streams.

- **How it fits Horizon**
  - Only needed when partners want continuous event feeds with sub-minute latency.
  - Streams:
    - Pharmacy events
    - Device telemetry
    - Event-level hospital usage

- **Implementation notes**
  - Start without Kafka; add it when you truly need streaming.
  - Use consumers that write to Postgres/TimescaleDB and trigger ML inference.

- **Key libraries / tools**
  - Apache Kafka (cluster)
  - Python:

    ```bash
    pip install confluent-kafka
    ```

### External Data Sources

- **Google Trends API / Health APIs**
  - Use HTTP clients (e.g., `requests`, `httpx`) or specific API wrappers.

- **CSV / Parquet Files**
  - Store raw files in object storage (e.g., S3 / GCS) for archival.
  - Load into Pandas and then into Postgres or a warehouse.

- **Key libraries**

  ```bash
  pip install requests httpx pandas pyarrow
  ```

---

## AI & Analytics Layer

This layer computes outbreak probabilities, detects anomalies, and generates risk scores that power dashboards and alerts.

### Core ML Stack: Python, Pandas, Scikit-Learn

- **What it does**
  - Handles feature engineering, model training, evaluation, and batch inference.

- **How it fits Horizon**
  - Transforms raw time-series data into features:
    - Rolling averages, week-over-week change, per-capita metrics.
  - Trains baseline models for outbreak risk classification and regression.

- **Implementation notes**
  - Standardize a project structure (e.g., `ml/` folder) for:
    - Data loading
    - Feature pipelines
    - Training scripts
    - Evaluation and validation
  - For large-scale historical training data:
    - Pull feature tables and training sets from **Snowflake** using the Snowflake Python connector.
    - Cache training data locally or in object storage as needed for experimentation.

- **Key libraries**

  ```bash
  pip install numpy pandas scikit-learn
  ```

### Gradient Boosting Models: XGBoost / LightGBM / CatBoost

- **What it does**
  - Provides high-performance models for tabular data and time-series features.

- **How it fits Horizon**
  - Primary models for:
    - Outbreak classification (probability of outbreak per region).
    - Risk scoring based on multiple indicators.

- **Implementation notes**
  - Use scikit-learn-compatible APIs to integrate with pipelines.
  - Train global models across tenants but allow per-tenant calibration (e.g., thresholds).

- **Key libraries**

  ```bash
  pip install xgboost lightgbm catboost
  ```

### Anomaly Detection: PyOD / River

- **What it does**
  - Detects unusual spikes or drops in health indicators.

- **How it fits Horizon**
  - Flags early anomalies in:
    - Pharmacy purchases
    - Specific search keywords
    - Supply usage patterns

- **Implementation notes**
  - Use **PyOD** for batch anomaly detection.
  - Use **River** for streaming/online anomaly detection if you add streaming.

- **Key libraries**

  ```bash
  pip install pyod river
  ```

### Deep Learning: TensorFlow or PyTorch (Optional)

- **What it does**
  - Supports more complex models (e.g., sequence models for multi-variate time series).

- **How it fits Horizon**
  - Use only when you’ve exhausted simpler models or need more expressive sequence modeling.

- **Implementation notes**
  - Start with one framework (TensorFlow or PyTorch) to avoid fragmentation.
  - Consider sequence models (LSTM/GRU/Transformers) if needed.

- **Key libraries**

  ```bash
  pip install tensorflow
  # or
  pip install torch torchvision torchaudio
  ```

### Experiment Tracking and Model Registry: MLflow

- **What it does**
  - Tracks experiments, parameters, metrics, and models.
  - Provides a model registry for versioning and deployment.

- **How it fits Horizon**
  - Helps you manage many iterations of outbreak and anomaly models.
  - Supports rollback to known-good models.

- **Implementation notes**
  - Run MLflow server as a separate service.
  - Track experiments from training scripts.
  - Register deployed models in the model registry with tags (e.g., `production`, `staging`).

- **Key libraries**

  ```bash
  pip install mlflow
  ```

---

## LLM / OpenRouter Reasoning Layer

This layer uses OpenRouter-hosted LLMs to provide natural-language interfaces, explanations, and summaries on top of Horizon’s numerical outputs.

### OpenRouter API Integration

- **What it does**
  - Provides access to multiple large language models via a unified HTTP API.
  - Powers:
    - Chat assistant in the dashboard.
    - Daily outbreak summaries.
    - Natural-language explanations of risk scores and anomalies.

- **How it fits Horizon**
  - Adds a “reasoning and explanation” layer:
    - Users can ask questions like:
      - “Why did Region X’s risk increase today?”
      - “Summarize high-risk areas for our hospital network this week.”
    - Clinical and executive users get narrative insights, not just charts.

- **Implementation notes**
  - Keep **core outbreak prediction inside your own ML stack**.
  - Use OpenRouter only on **aggregated, non-identifiable data** (no raw PHI).
  - Implement an internal service (e.g., `llm_service`) in your backend that:
    - Fetches structured data from your DB.
    - Constructs safe prompts for the LLM.
    - Calls OpenRouter via HTTPS.
    - Returns formatted text to the frontend.
  - Store the OpenRouter API key in environment variables (e.g., `OPENROUTER_API_KEY`).

- **Key libraries**
  - You can use any HTTP client; recommended:

  ```bash
  pip install httpx
  # or
  pip install requests
  ```

  - Basic usage pattern (conceptual):

  ```python
  import httpx

  async def call_openrouter(prompt: str) -> str:
      headers = {
          "Authorization": f"Bearer {OPENROUTER_API_KEY}",
          "Content-Type": "application/json",
      }
      payload = {
          "model": "openai/gpt-4.1-mini",  # example; choose model via OpenRouter
          "messages": [{"role": "user", "content": prompt}],
      }
      async with httpx.AsyncClient() as client:
          resp = await client.post("https://openrouter.ai/api/v1/chat/completions",
                                   json=payload,
                                   headers=headers,
                                   timeout=30)
      resp.raise_for_status()
      return resp.json()["choices"][0]["message"]["content"]
  ```

---

## Backend API & Integration Layer

This layer exposes Horizon’s capabilities to the frontend and to external partners (hospitals, health systems, insurers, etc.).

### FastAPI Backend

- **What it does**
  - Provides REST (and optionally WebSocket) APIs for:
    - Risk scores
    - Anomaly data
    - Alert management
    - FinTech simulation triggers
    - LLM/OpenRouter endpoints

- **How it fits Horizon**
  - Core server for:
    - Multi-tenant access (per-organization).
    - Auth and authorization checks.
    - Integration with external systems via APIs and webhooks.

- **Implementation notes**
  - Define routers for:
    - `/health/metrics`
    - `/risk/scores`
    - `/alerts`
    - `/fintech/allocations`
    - `/llm/query`
  - Use Pydantic models for request/response validation.
  - Connect to Postgres via SQLAlchemy.
  - Containerize with Docker and deploy to Kubernetes or a managed service.

- **Key libraries**

  ```bash
  pip install fastapi uvicorn[standard] pydantic sqlalchemy
  ```

### Integration with Hospital / Company Systems

- **What it does**
  - Enables Horizon to consume organizational data and send back insights.

- **How it fits Horizon**
  - Ingests:
    - Aggregated, de-identified clinical data.
    - Operational metrics (admissions, supply usage).
  - Returns:
    - Outbreak risk scores.
    - Alerts, recommended actions, and FinTech allocations.

- **Implementation notes**
  - For modern systems:
    - Implement FHIR-based APIs where possible.
  - For legacy environments:
    - Use CSV/SFTP ingestion pipelines.
  - Expose webhooks for pushing alerts back into partner systems.

- **Key libraries**
  - Same as FastAPI + integration-specific SDKs if needed.

---

## Dashboard / Frontend Layer

This layer provides interactive visualizations, heatmaps, and a conversational assistant UI.

### React Frontend

- **What it does**
  - Implements the main Horizon dashboard for hospitals and healthcare companies.

- **How it fits Horizon**
  - Displays:
    - Real-time heatmaps of outbreak risk.
    - Trend charts over time.
    - Organization-specific views and filters.
  - Includes:
    - A chat-style **“Horizon Assistant”** powered by OpenRouter.

- **Implementation notes**
  - Use React with TypeScript for maintainability.
  - Communicate with the FastAPI backend via REST (e.g., using `axios` or `fetch`).
  - Use a map library for geospatial visualization.
  - Implement role-based UI (admin, clinician, analyst, exec).

- **Key libraries / tools**

  ```bash
  # assuming Node.js and a React scaffold (Vite / Next.js / CRA)
  npm install react react-dom
  npm install axios
  npm install recharts        # or another charting lib
  npm install mapbox-gl       # or leaflet
  ```

### Streamlit (Internal Tools / Prototyping)

- **What it does**
  - Provides quick, Python-native dashboards for data scientists and internal stakeholders.

- **How it fits Horizon**
  - For internal experimentation:
    - Rapid prototyping of new features and models.
    - Debugging data and visualizing intermediate outputs.

- **Implementation notes**
  - Do not rely on Streamlit for the production, multi-tenant customer dashboard.
  - Use it primarily in development and internal analytics.

- **Key libraries**

  ```bash
  pip install streamlit
  ```

---

## FinTech Simulation Layer

This layer simulates and eventually triggers financial responses based on outbreak risk.

### Risk-to-Funds Engine (Python Service)

- **What it does**
  - Implements business rules like:
    - “If outbreak probability > X% for region Y, allocate Z units of emergency funds.”

- **How it fits Horizon**
  - Computes:
    - Recommended fund allocations by region and organization.
    - Potential impact on costs and resources.

- **Implementation notes**
  - Implement as a separate FastAPI microservice or as a module in the main backend.
  - Uses data from the AI layer (risk scores) and financial configurations per tenant.
  - Writes results to a “funds ledger” table in Postgres.
  - Optionally triggers notifications or downstream integrations (e.g., webhooks).

- **Key libraries**
  - Same as FastAPI backend; optionally:

  ```bash
  pip install celery redis
  ```

  for asynchronous job processing.

### Future On-Chain / Financial Integrations (Optional)

- **What it does**
  - Connects simulated decisions to real financial systems or smart contracts.

- **How it fits Horizon**
  - For customers who want automated, financial workflows based on risk.

- **Implementation notes**
  - Start with internal simulation only.
  - Later, integrate with:
    - Banking APIs / payment rails.
    - Smart contracts using Solidity/Vyper if blockchain is truly needed.

- **Key libraries / tools**
  - Depends on chosen finance/chain stack; e.g., `web3.py` for EVM chains.

---

## Infrastructure, Security, and DevOps

### Containerization and Orchestration

- **What it does**
  - Packages services into containers and orchestrates them in production.

- **How it fits Horizon**
  - Enables scalable deployment for:
    - FastAPI backend
    - ML inference services
    - Airflow/Prefect
    - Streamlit (internal) and other utilities

- **Implementation notes**
  - Use Docker for container images.
  - Orchestrate with Kubernetes (K8s) or managed alternatives (e.g., GKE, EKS, AKS) or serverless containers (Cloud Run).

- **Key tools**
  - Docker, Kubernetes, Helm (optional).

### Authentication / Authorization

- **What it does**
  - Secures Horizon as a multi-tenant SaaS.

- **How it fits Horizon**
  - Ensures only authorized users from each organization can access their data.

- **Implementation notes**
  - Use a managed identity provider:
    - Auth0, AWS Cognito, or similar.
  - Implement roles:
    - Admin, clinician, analyst, exec.
  - Pass `tenant_id` (organization ID) in JWT claims and enforce in the backend via RBAC and row-level security in the database.

### Security, Privacy, and Compliance

- **What it does**
  - Protects sensitive health-related data and meets regulatory requirements.

- **How it fits Horizon**
  - Critical for hospital and healthcare company adoption.

- **Implementation notes**
  - Use TLS (HTTPS) everywhere.
  - Encrypt data at rest via managed DBs.
  - Avoid sending PHI to OpenRouter or external LLMs.
  - Implement auditing and logging for data access.

---

## Summary

- The stack centers around **Python + Postgres/TimescaleDB + Snowflake + FastAPI + React**, with **OpenRouter** as a reasoning and explanation layer.
- Each technology in this document includes its role, integration into Horizon, implementation notes, and key libraries/tools to install.
- This setup supports **large-scale, multi-tenant, near real-time outbreak detection** with a modern dashboard, integrable APIs, and AI-powered narrative insights.


