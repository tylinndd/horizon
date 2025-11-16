# Horizon - Outbreak Detection & Risk Assessment Platform

Horizon is a production-ready AI-powered platform for detecting disease outbreaks, assessing health risks, and optimizing hospital resource allocation in real-time. Built with modern technologies and designed for healthcare organizations, public health agencies, and hospital systems.

## ✨ Key Features

### 🎯 Real-Time Risk Assessment
- **ML-Powered Risk Scoring**: Multi-factor outbreak risk assessment by region
- **Anomaly Detection**: Early detection of unusual patterns in health indicators
- **Risk Visualization**: Interactive color-coded risk map showing regional threats
- **Predictive Analytics**: Forecast outbreak trends and resource demands

### 🏥 Hospital Intelligence
- **Integrated Dashboard**: Comprehensive hospital operations overview (Emory Hospital integration)
- **Budget Management**: Track and optimize hospital budget allocations
- **Resource Optimization**: AI-powered recommendations for capacity planning
- **Financial Impact Analysis**: Cost-benefit analysis for operational decisions

### 🚨 Alert Management
- **Automated Alerts**: Real-time notifications for high-risk situations
- **Severity Classification**: Critical, high, medium, and low priority alerts
- **Alert Acknowledgment**: Track alert status and response times
- **Filtering & Search**: Quickly find relevant alerts by region, severity, or status

### 🤖 AI Assistant
- **Natural Language Queries**: Ask questions in plain English
- **Context-Aware Responses**: Leverages real-time data for accurate answers
- **Risk Explanations**: Detailed breakdowns of risk score calculations
- **Actionable Insights**: Data-driven recommendations for decision-makers

### 📊 Data & Analytics
- **Time-Series Analysis**: Historical trend visualization with interactive charts
- **Multi-Source Data Integration**: CDC data, pharmacy trends, hospital metrics
- **ETL Pipelines**: Automated data ingestion and processing
- **Multi-Tenant Support**: Organization-level data isolation

### 🎨 Modern UI/UX
- **Clean Design**: Minimalist white/black/red color scheme
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Interactive Visualizations**: Charts, maps, and real-time dashboards
- **Modal Details**: Click-to-expand detailed information views

## 🛠 Tech Stack

### Backend
- **FastAPI** 0.104+ - Modern async Python web framework
- **PostgreSQL** 15+ - Relational database
- **TimescaleDB** - Time-series database extension
- **SQLAlchemy** 2.0+ - ORM for database operations
- **Alembic** - Database migration tool
- **Prefect** 2.14+ - Workflow orchestration for ETL
- **OpenRouter** - Multi-model LLM API access

### Frontend
- **React** 18+ with **TypeScript** - Modern UI framework with type safety
- **Vite** 5+ - Lightning-fast build tool
- **Recharts** 2.5+ - Data visualization library
- **Axios** - HTTP client for API communication
- **React Router** 6+ - Client-side routing

### ML/AI
- **Scikit-learn** 1.3+ - Machine learning algorithms
- **XGBoost** 2.0+ - Gradient boosting models
- **PyOD** 1.1+ - Outlier/anomaly detection
- **NumPy** & **Pandas** - Data processing and analysis
- **MLflow** 2.9+ - ML experiment tracking
- **OpenAI GPT-4** / **Claude** - Advanced language models via OpenRouter

### Infrastructure
- **Docker** & **Docker Compose** - Containerization
- **Nginx** - Web server and reverse proxy
- **Gunicorn/Uvicorn** - Python application servers

### Optional/Future
- **Snowflake** - Cloud data warehouse (configured, not yet deployed)
- **Redis** - Caching layer (planned)
- **Grafana** - Monitoring dashboards (planned)

> 📖 **For comprehensive feature documentation and technology mapping, see [FEATURES.md](FEATURES.md)**

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

## 📱 Application Pages

### 🏠 Homepage
Clean landing page with platform introduction and navigation.

### 📊 Dashboard
Central command center showing:
- Risk overview with critical/high-risk regions
- Recent alerts panel
- Emory Hospital integrated intelligence
- Budget overview with visual cards
- Resource allocation recommendations
- AI-powered recommendations
- Risk trend charts (line/bar toggle, time range selection)
- Horizon Assistant chat interface

### 🗺️ Risk Map
Interactive visualization showing:
- Regional outbreak risk levels
- Color-coded severity indicators
- Click-to-view region details
- Filter by risk level

### 🚨 Alerts Page
Comprehensive alert management:
- All alerts with severity badges
- Filter by severity (critical/high/medium/low)
- Filter by read/unread status
- Mark as read and acknowledge actions
- Detailed alert information

### 🏥 Emory Hospital
Hospital-specific intelligence dashboard:
- Facility overview with regional risk
- Budget management and tracking
- Resource capacity analysis
- AI-powered operational recommendations
- Financial impact projections

### 🌐 Platform
Information about platform capabilities and integrations.

## 🔌 API Endpoints

### Health Metrics
- `GET /api/health/metrics` - Get health metrics with filters
- `GET /api/health/search-trends` - Google Trends symptom searches
- `GET /api/health/pharmacy` - Pharmacy medication purchase data
- `GET /api/health/hospital-utilization` - Hospital capacity and utilization

### Risk Scores & Anomalies
- `GET /api/risk/scores` - Historical risk scores (filterable by region, date, level)
- `GET /api/risk/scores/latest` - Current risk scores for all regions
- `GET /api/risk/anomalies` - Detected anomalies in health indicators

### Alerts
- `GET /api/alerts` - Get alerts (filter by severity, status, region)
- `PATCH /api/alerts/{id}/read` - Mark alert as read
- `PATCH /api/alerts/{id}/acknowledge` - Acknowledge alert

### Hospital Intelligence
- `GET /api/hospital/dashboard/{facility_id}` - Complete hospital dashboard data
- `GET /api/hospital/budget/{facility_id}` - Budget information and recommendations
- `GET /api/hospital/resources/{facility_id}` - Resource allocation insights
- `GET /api/hospital/recommendations/{facility_id}` - AI-powered recommendations

### FinTech Simulation
- `GET /api/fintech/allocations` - Fund allocation simulations

### LLM / AI Assistant
- `POST /api/llm/query` - Natural language query to Horizon Assistant
- `POST /api/llm/explain-risk` - Get detailed risk score explanation

> 📚 **Interactive API Documentation:** http://localhost:8000/docs (Swagger UI)

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

## 📚 Documentation

- **[FEATURES.md](FEATURES.md)** - Comprehensive feature list with technology mapping
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview and implementation details
- **[TECH_STACK.md](TECH_STACK.md)** - Detailed technology stack documentation
- **[SETUP.md](SETUP.md)** - Detailed setup and configuration guide
- **[DATA_SOURCES.md](DATA_SOURCES.md)** - Data sources and integration guide
- **[HACKATHON_GUIDE.md](HACKATHON_GUIDE.md)** - Hackathon-specific guide and demos
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions
- **API Documentation:** http://localhost:8000/docs (when running)

## 🌟 What Makes Horizon Special

1. **Multi-Faceted Risk Assessment**
   - Combines multiple data sources (search trends, pharmacy data, hospital metrics)
   - ML-powered anomaly detection catches early outbreak signals
   - Real-time risk scoring updated continuously

2. **Hospital Integration**
   - First platform to integrate outbreak detection with hospital operations
   - AI-powered budget and resource recommendations
   - Financial impact analysis for operational decisions

3. **Production-Ready Architecture**
   - Modern async Python backend with FastAPI
   - Time-series optimized database with TimescaleDB
   - Containerized deployment with Docker
   - Scalable ETL pipelines with Prefect

4. **AI-Powered Intelligence**
   - Natural language assistant using state-of-the-art LLMs
   - Context-aware responses based on real-time data
   - Explainable AI for risk score transparency

5. **Clean, Intuitive UI**
   - Minimalist design focused on critical information
   - Responsive across all devices
   - Interactive visualizations for better insights

6. **Enterprise Features**
   - Multi-tenant architecture for multiple organizations
   - Comprehensive API for integrations
   - Audit trails for all actions
   - Export and reporting capabilities

## 🎯 Use Cases

### Public Health Agencies
- Monitor outbreak risks across jurisdictions
- Early warning system for disease outbreaks
- Data-driven resource allocation decisions
- Population health trend analysis

### Hospital Systems
- Optimize resource allocation based on risk levels
- Budget planning with AI recommendations
- Capacity planning for surge scenarios
- Supply chain optimization

### Healthcare Organizations
- Track regional health trends
- Predict resource demands
- Coordinate response efforts
- Generate compliance reports

### Research Institutions
- Access to aggregated health data
- Study outbreak patterns
- Test predictive models
- Publish findings

## 🔒 Security & Compliance

- **Multi-Tenant Data Isolation** - Organization-level data separation
- **Input Validation** - All inputs validated with Pydantic
- **SQL Injection Prevention** - ORM-based database access
- **CORS Configuration** - Controlled API access
- **Environment-based Secrets** - No hardcoded credentials
- **Future:** HIPAA compliance, SOC2 certification, encryption at rest/transit

## 🚀 Roadmap

### Q1 2025
- [ ] Real-time websocket notifications
- [ ] Mobile app (React Native)
- [ ] Advanced geospatial visualization (Mapbox)
- [ ] User authentication & RBAC
- [ ] Email/SMS alert notifications

### Q2 2025
- [ ] Snowflake data warehouse integration
- [ ] BI tool connectors (Tableau, PowerBI)
- [ ] Advanced ML model training UI
- [ ] GraphQL API
- [ ] Multi-language support

### Q3 2025
- [ ] Automated testing suite
- [ ] Performance monitoring dashboard
- [ ] Integration marketplace
- [ ] White-label capabilities
- [ ] Enterprise SLA support

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for TypeScript/React
- Write tests for new features
- Update documentation as needed

## 📧 Support

For questions, issues, or feature requests:
- **GitHub Issues:** [Create an issue](https://github.com/your-org/horizon/issues)
- **Email:** support@horizon-platform.com
- **Documentation:** See docs above

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- **CDC & OWID** for public health data
- **OpenRouter** for LLM API access
- **TimescaleDB** for time-series database technology
- **FastAPI** community for excellent documentation
- **React** and **TypeScript** communities

---

**Built with ❤️ for public health**

*Horizon - Detecting outbreaks before they become crises.*
