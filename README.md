# Horizon - Outbreak Detection Platform

Horizon is a production-ready platform for detecting outbreaks and assessing health risks using AI, ML, and real-time data analytics.

## Features

- **Real-time Risk Scoring**: ML-powered outbreak risk assessment by region
- **Anomaly Detection**: Early detection of unusual patterns in health indicators
- **Interactive Dashboard**: Clean, modern UI with white/black/red theme
- **Risk Heatmap**: Visual representation of outbreak risks across regions
- **Alert System**: Real-time alerts for high-risk situations
- **Horizon Assistant**: AI-powered chat assistant using OpenRouter LLM
- **Multi-tenant Support**: Organization-level data isolation
- **ETL Pipelines**: Automated data ingestion from multiple sources

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL + TimescaleDB**: Time-series database
- **SQLAlchemy + Alembic**: ORM and migrations
- **Prefect**: ETL orchestration
- **OpenRouter**: LLM integration

### Frontend
- **React + TypeScript**: Modern frontend framework
- **Vite**: Fast build tool
- **Recharts**: Data visualization
- **Axios**: HTTP client

### ML/AI
- **Scikit-learn**: Machine learning
- **XGBoost/LightGBM**: Gradient boosting models
- **PyOD**: Anomaly detection
- **MLflow**: Experiment tracking

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15+ with TimescaleDB extension

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd horizon
```

2. Create a `.env` file in the backend directory:
```bash
cd backend
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

3. Start all services:
```bash
docker compose up -d
```
   (Note: If you have an older Docker installation, you may need to use `docker-compose` instead)

4. Run database migrations:
```bash
docker compose exec backend alembic upgrade head
```

5. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```bash
# Install TimescaleDB extension
psql -U horizon -d horizon -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Project Structure

```
horizon/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   └── etl/          # ETL flows
│   ├── alembic/          # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
│   └── package.json
└── docker-compose.yml
```

## API Endpoints

### Health Metrics
- `GET /api/health/metrics` - Get health metrics
- `GET /api/health/search-trends` - Get search trends
- `GET /api/health/pharmacy` - Get pharmacy metrics
- `GET /api/health/hospital-utilization` - Get hospital utilization

### Risk Scores
- `GET /api/risk/scores` - Get risk scores
- `GET /api/risk/scores/latest` - Get latest risk scores
- `GET /api/risk/anomalies` - Get detected anomalies

### Alerts
- `GET /api/alerts` - Get alerts
- `PATCH /api/alerts/{id}/read` - Mark alert as read
- `PATCH /api/alerts/{id}/acknowledge` - Acknowledge alert

### FinTech
- `GET /api/fintech/allocations` - Get fund allocations

### LLM
- `POST /api/llm/query` - Query Horizon Assistant
- `POST /api/llm/explain-risk` - Get risk explanation

## Running ETL Flows

To run Prefect ETL flows for data ingestion:

```bash
cd backend
python -m app.etl.flows
```

Or schedule them with Prefect Cloud/Server:

```bash
prefect deploy app/etl/flows.py:ingest_public_data_flow
prefect deploy app/etl/flows.py:ingest_synthetic_data_flow
```

## Environment Variables

### Backend (.env)

```bash
DATABASE_URL=postgresql://horizon:horizon@localhost:5432/horizon
OPENROUTER_API_KEY=your-api-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
SECRET_KEY=your-secret-key
MLFLOW_TRACKING_URI=http://localhost:5000
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
black app/
isort app/

# Frontend
npm run lint
```

## License

[Your License Here]

## Contributing

[Contributing Guidelines]
