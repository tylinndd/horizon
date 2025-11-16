# Horizon - Complete Features & Technologies Documentation

This document provides a comprehensive overview of every feature in Horizon and the technologies powering each one.

---

## Table of Contents

1. [Frontend Features](#frontend-features)
2. [Backend Features](#backend-features)
3. [Data & Analytics Features](#data--analytics-features)
4. [AI/ML Features](#aiml-features)
5. [Hospital Intelligence Features](#hospital-intelligence-features)
6. [Infrastructure & DevOps](#infrastructure--devops)
7. [Technology Stack Summary](#technology-stack-summary)

---

## Frontend Features

### 1. **Homepage / Landing Page**
**Location:** `frontend/src/pages/Homepage.tsx`

**What it does:**
- Modern landing page introducing Horizon
- Hero section with call-to-action
- Feature highlights and platform overview
- Navigation to main application

**Technologies:**
- React 18+ with TypeScript
- CSS3 for styling
- React Router for navigation

---

### 2. **Interactive Dashboard**
**Location:** `frontend/src/pages/Dashboard.tsx`

**What it does:**
- Central command center showing all critical metrics
- Real-time risk overview with color-coded severity (low, medium, high, critical)
- Recent alerts panel with filtering
- Risk trend visualization with charts
- AI assistant integration
- Emory Hospital integrated intelligence dashboard

**Components:**
- Risk overview cards showing critical/high-risk regions
- Alert cards with severity indicators
- Trend charts (line and bar chart toggles)
- Time range filters (7 days, 30 days)
- Region-specific filtering
- Budget overview with allocation breakdown
- Resource allocation recommendations
- AI-powered recommendations panel

**Technologies:**
- **React 18+** with TypeScript
- **Recharts** - Data visualization library for trend charts
  - LineChart for time-series risk data
  - BarChart for comparative metrics
  - CartesianGrid, XAxis, YAxis for chart components
- **Axios** - HTTP client for API calls
- **CSS Grid & Flexbox** - Responsive layout
- Real-time data fetching with 5-minute auto-refresh

**API Endpoints Used:**
- `/api/risk/scores/latest` - Get latest risk scores
- `/api/alerts` - Fetch recent alerts
- `/api/risk/scores` - Historical risk data for trends
- `/api/hospital/dashboard/{facility_id}` - Hospital insights

---

### 3. **Risk Map**
**Location:** `frontend/src/pages/RiskMap.tsx`

**What it does:**
- Visual representation of outbreak risks across regions
- Color-coded regions based on risk severity
- Interactive region selection
- Risk score details on hover/click
- Filter by risk level
- Time-based analysis

**Technologies:**
- React with TypeScript
- SVG-based map rendering
- CSS animations for hover effects
- Color gradients for risk visualization
  - Red (`#dc2626`) - Critical risk
  - Orange (`#ea580c`) - High risk  
  - Yellow (`#fbbf24`) - Medium risk
  - Gray (`#e5e5e5`) - Low risk

**API Endpoints Used:**
- `/api/risk/scores/latest` - Current regional risk scores

---

### 4. **Alerts Management Page**
**Location:** `frontend/src/pages/Alerts.tsx`

**What it does:**
- Comprehensive alert management system
- Filter alerts by severity (critical, high, medium, low)
- Filter by read/unread status
- Mark alerts as read
- Acknowledge alerts
- Detailed alert information display
- Real-time alert notifications

**Technologies:**
- React with TypeScript
- State management with useState hooks
- Real-time updates with polling
- CSS filtering and sorting UI

**API Endpoints Used:**
- `/api/alerts` - Fetch alerts with filters
- `/api/alerts/{id}/read` - Mark alert as read
- `/api/alerts/{id}/acknowledge` - Acknowledge alert

---

### 5. **Platform Overview Page**
**Location:** `frontend/src/pages/Platform.tsx`

**What it does:**
- Detailed platform capabilities showcase
- Feature explanations
- Technology stack information
- Integration possibilities

**Technologies:**
- React with TypeScript
- Responsive design with CSS Grid

---

### 6. **Emory Hospital Intelligence Dashboard**
**Location:** `frontend/src/pages/EmoryHospital.tsx`

**What it does:**
- Hospital-specific integrated dashboard
- Budget tracking and management
- Resource allocation insights
- Risk-adjusted recommendations
- Financial impact analysis
- Real-time hospital metrics

**Technologies:**
- React with TypeScript
- Recharts for hospital metrics visualization
- Real-time data synchronization

**API Endpoints Used:**
- `/api/hospital/dashboard/{facility_id}` - Comprehensive hospital data
- `/api/hospital/budget/{facility_id}` - Budget information
- `/api/hospital/resources/{facility_id}` - Resource allocations
- `/api/hospital/recommendations/{facility_id}` - AI recommendations

---

### 7. **Reusable Components**

#### Risk Score Card
**Location:** `frontend/src/components/RiskScoreCard.tsx`

**Features:**
- Color-coded risk display
- Region identification
- Risk probability percentage
- Contributing factors display
- Click-to-expand details

**Technologies:**
- React functional component
- Dynamic styling based on risk level
- Tooltip integration

#### Alert Card
**Location:** `frontend/src/components/AlertCard.tsx`

**Features:**
- Severity badge display
- Alert type indicator
- Timestamp formatting
- Read/unread status
- Interactive actions

**Technologies:**
- React functional component
- Date formatting with JavaScript Date API

#### Trend Chart
**Location:** `frontend/src/components/TrendChart.tsx`

**Features:**
- Line and bar chart toggle
- Time range selection (7/30 days)
- Region-specific filtering
- Data aggregation by date
- Sample data generation fallback
- Responsive container

**Technologies:**
- Recharts library
- ResponsiveContainer for adaptive sizing
- Custom tooltips and legends

#### Horizon Assistant (AI Chat)
**Location:** `frontend/src/components/HorizonAssistant.tsx`

**Features:**
- Natural language query interface
- Context-aware responses
- Risk score explanations
- Real-time chat interface
- Message history
- Typing indicators
- Quick action buttons

**Technologies:**
- React with useState for message management
- Axios for LLM API calls
- CSS animations for typing indicators

**API Endpoints Used:**
- `/api/llm/query` - General queries
- `/api/llm/explain-risk` - Risk explanations

#### Card Modal
**Location:** `frontend/src/components/CardModal.tsx`

**Features:**
- Reusable modal dialog
- Detailed information display
- Click-outside to close
- Smooth animations
- Responsive design

**Technologies:**
- React Portal API
- CSS transitions
- Event handling for close actions

#### Layout & Navigation
**Location:** `frontend/src/components/Layout.tsx`

**Features:**
- Consistent navigation header
- Active route highlighting
- Responsive menu
- Horizon branding

**Technologies:**
- React Router DOM
- NavLink for active states
- CSS flexbox layout

---

## Backend Features

### 1. **Health Metrics API**
**Location:** `backend/app/api/health.py`

**Endpoints:**

#### `GET /api/health/metrics`
- Fetch general health metrics
- Filter by region, date range
- Multi-tenant support

#### `GET /api/health/search-trends`
- Google Trends search data
- Symptom-related searches by region
- Time-series data

#### `GET /api/health/pharmacy`
- Pharmacy medication purchase aggregates
- Over-the-counter medication trends
- Regional pharmacy metrics

#### `GET /api/health/hospital-utilization`
- Hospital capacity metrics
- Bed utilization rates
- PPE and supply usage

**Technologies:**
- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and serialization
- **PostgreSQL** - Relational database storage
- **TimescaleDB** - Time-series optimization

**Database Models:**
- `SearchTrend`
- `PharmacyAggregate`
- `HospitalUtilization`
- `OWIDCovidMetric`

---

### 2. **Risk Scoring API**
**Location:** `backend/app/api/risk.py`

**Endpoints:**

#### `GET /api/risk/scores`
- Historical risk scores
- Filter by region, date range, risk level
- Pagination support

#### `GET /api/risk/scores/latest`
- Current risk scores for all regions
- Real-time risk assessment
- Color-coded severity levels

#### `GET /api/risk/anomalies`
- Detected anomalies in health indicators
- Anomaly type classification
- Severity ratings

**Technologies:**
- FastAPI
- SQLAlchemy ORM
- Machine Learning integration (calls `ml_service.py`)
- Real-time scoring algorithms

**Database Models:**
- `RiskScore` - Computed risk assessments
- `Anomaly` - Detected anomalies

---

### 3. **Alert Management API**
**Location:** `backend/app/api/alerts.py`

**Endpoints:**

#### `GET /api/alerts`
- Fetch alerts with filtering
- Filter by severity, read status, region
- Pagination support

#### `PATCH /api/alerts/{id}/read`
- Mark alert as read
- Update read timestamp

#### `PATCH /api/alerts/{id}/acknowledge`
- Acknowledge alert
- Track acknowledgment user/time

**Technologies:**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Automated alert generation based on risk thresholds

**Database Models:**
- `Alert` - System-generated alerts

---

### 4. **Hospital Intelligence API**
**Location:** `backend/app/api/hospital.py`

**Endpoints:**

#### `GET /api/hospital/dashboard/{facility_id}`
- Comprehensive hospital dashboard data
- Budget information
- Resource allocations
- AI-powered recommendations
- Risk scores

#### `GET /api/hospital/budget/{facility_id}`
- Budget breakdown by category
- Risk-adjusted budget recommendations
- Period-based budget tracking

#### `GET /api/hospital/resources/{facility_id}`
- Resource allocation recommendations
- Current vs recommended capacity
- Utilization rates
- Priority levels

#### `GET /api/hospital/recommendations/{facility_id}`
- AI-powered operational recommendations
- Cost-benefit analysis
- Implementation timeframes
- Estimated savings

**Technologies:**
- FastAPI
- SQLAlchemy
- PostgreSQL
- ML-powered recommendation engine

**Database Models:**
- `HospitalBudget`
- `ResourceAllocation`
- `HospitalRecommendation`

---

### 5. **FinTech Simulation API**
**Location:** `backend/app/api/fintech.py`

**Endpoints:**

#### `GET /api/fintech/allocations`
- Fund allocation simulations
- Risk-based resource distribution
- Budget optimization recommendations

**Technologies:**
- FastAPI
- Financial modeling algorithms
- Risk-based allocation strategies

**Database Models:**
- `FundAllocation`

---

### 6. **LLM / AI Assistant API**
**Location:** `backend/app/api/llm.py`

**Endpoints:**

#### `POST /api/llm/query`
- Natural language query processing
- Context-aware responses
- Data-driven insights

**Request Body:**
```json
{
  "query": "What is the current risk in Atlanta?",
  "context": {
    "riskScores": [...],
    "alerts": [...]
  }
}
```

#### `POST /api/llm/explain-risk`
- Detailed risk score explanations
- Contributing factors analysis
- Actionable recommendations

**Request Body:**
```json
{
  "region_id": "atlanta-ga",
  "risk_score": 0.75,
  "risk_level": "high"
}
```

**Technologies:**
- **OpenRouter** - LLM API aggregator
- Supports multiple models:
  - OpenAI GPT-4
  - Anthropic Claude
  - Google Gemini
  - Meta Llama
- **HTTPX** - Async HTTP client
- Prompt engineering for healthcare context
- Context injection for accurate responses

**Implementation:**
- Location: `backend/app/services/llm_service.py`
- Configurable model selection
- Rate limiting and error handling
- Response streaming support

---

## Data & Analytics Features

### 1. **TimescaleDB Integration**

**What it does:**
- Time-series database optimization
- Efficient storage of temporal health data
- Fast aggregation queries
- Automatic data retention policies

**Use Cases:**
- Storing historical risk scores
- Time-based pharmacy trends
- Hospital utilization over time
- Search trend analysis

**Technologies:**
- PostgreSQL 15+ with TimescaleDB extension
- Hypertables for time-series data
- Continuous aggregates for pre-computed rollups
- Data retention policies

**Implementation:**
- Tables optimized as hypertables
- Indexes on time columns
- Partitioning by time for performance

---

### 2. **ETL Pipeline (Prefect)**
**Location:** `backend/app/etl/`

**Flows:**

#### Public Data Ingestion Flow
- Fetches data from public health APIs
- OWID (Our World in Data) COVID metrics
- Google Trends symptom searches
- Scheduled execution

#### Synthetic Data Generation Flow
- Generates test data for development
- Realistic pharmacy patterns
- Hospital utilization simulations
- Anomaly injection for testing

**Technologies:**
- **Prefect 2.14+** - Modern workflow orchestration
- Task scheduling and monitoring
- Retry logic and error handling
- Data quality validation
- **Pandas** - Data manipulation
- **Requests** - HTTP data fetching
- **PyTrends** - Google Trends API

**Scheduling:**
- Configurable cron schedules
- Manual triggering support
- Prefect Cloud/Server integration

---

### 3. **Database Schema & Models**
**Location:** `backend/app/models/`

**Models:**

#### Health Metrics (`health_metrics.py`)
- `HealthMetric` - Base class with multi-tenancy
- `SearchTrend` - Google search trends
- `PharmacyAggregate` - Medication purchases
- `HospitalUtilization` - Capacity metrics
- `OWIDCovidMetric` - Public health data

#### Risk Scores (`risk_scores.py`)
- `RiskScore` - Computed outbreak risk
- `Anomaly` - Detected anomalies

#### Alerts (`alerts.py`)
- `Alert` - System-generated notifications

#### Hospital Insights (`hospital_insights.py`)
- `HospitalBudget` - Financial tracking
- `ResourceAllocation` - Capacity planning
- `HospitalRecommendation` - AI suggestions

#### FinTech (`fintech.py`)
- `FundAllocation` - Resource distribution

**Features:**
- Multi-tenant architecture (`tenant_id` field)
- Proper indexing for performance
- Foreign key relationships
- Timestamp tracking
- JSON fields for flexible data

**Technologies:**
- SQLAlchemy 2.0+ ORM
- Alembic for migrations
- PostgreSQL data types
- TimescaleDB extensions

---

### 4. **Data Ingestion Scripts**
**Location:** `backend/scripts/`

**Scripts:**

#### `ingest_local_datasets.py`
- Ingests CSV files from local datasets folder
- Supports CDC data files
- Hospital utilization data
- Influenza surveillance data

#### `generate_emory_hospital_data.py`
- Generates Emory Hospital sample data
- Budget allocations
- Resource recommendations
- Risk scenarios

#### `seed_data.py`
- Seeds database with initial data
- Creates sample regions
- Generates test scenarios

**Technologies:**
- Python scripts
- Pandas for CSV processing
- SQLAlchemy for database insertion
- Error handling and logging

---

## AI/ML Features

### 1. **Machine Learning Service**
**Location:** `backend/app/services/ml_service.py`

**Capabilities:**

#### Risk Scoring Model
- Multi-factor risk assessment
- Regional outbreak probability calculation
- Severity classification (low, medium, high, critical)
- Contributing factors identification

**Algorithm:**
- Ensemble approach combining:
  - Search trend analysis
  - Pharmacy purchase patterns
  - Hospital utilization rates
  - Historical outbreak patterns
- Weighted scoring system
- Threshold-based classification

#### Anomaly Detection
- Time-series anomaly detection
- Statistical outlier identification
- Pattern deviation alerts
- Real-time anomaly flagging

**Algorithms:**
- **Isolation Forest** - Unsupervised anomaly detection
- **Local Outlier Factor (LOF)** - Density-based detection
- **PyOD library** - Multiple detector ensemble

#### Predictive Analytics
- Outbreak trend forecasting
- Resource demand prediction
- Capacity planning support

**Technologies:**
- **Scikit-learn** - ML framework
  - Random Forest Classifier
  - Isolation Forest
  - Standard Scaler for normalization
- **XGBoost** - Gradient boosting
- **PyOD** - Outlier detection
- **NumPy** - Numerical computing
- **Pandas** - Data preprocessing
- **MLflow** - Experiment tracking (optional)

**Features:**
- Model versioning
- Feature engineering pipelines
- Cross-validation
- Performance metrics tracking
- Model retraining capabilities

---

### 2. **LLM Service (AI Assistant)**
**Location:** `backend/app/services/llm_service.py`

**Capabilities:**

#### Natural Language Understanding
- Parse user queries
- Extract intent and entities
- Context-aware responses

#### Data Querying
- Translate natural language to database queries
- Aggregate and summarize data
- Generate insights from patterns

#### Explanations & Recommendations
- Explain risk score calculations
- Provide actionable recommendations
- Contextualize alerts and anomalies

**Technologies:**
- **OpenRouter API** - Multi-model LLM access
- Supported models:
  - `openai/gpt-4o-mini` (default)
  - `anthropic/claude-3.5-sonnet`
  - `google/gemini-pro`
  - `meta-llama/llama-3-70b`
- **HTTPX** - Async HTTP client
- Prompt templates for healthcare context
- Response parsing and formatting

**Implementation Details:**
- Streaming responses
- Token management
- Error handling and retries
- Rate limiting
- Cost optimization

---

### 3. **Hospital Recommendation Engine**

**What it does:**
- Analyzes hospital operations data
- Generates AI-powered recommendations
- Calculates cost-benefit analysis
- Prioritizes actions based on impact

**Recommendation Types:**
- Budget reallocation
- Resource capacity adjustments
- Equipment procurement
- Staffing optimization
- Infrastructure improvements

**Technologies:**
- Custom algorithms combining:
  - Risk scores
  - Utilization rates
  - Budget constraints
  - Historical patterns
- Decision tree logic
- Optimization algorithms

---

## Hospital Intelligence Features

### 1. **Budget Management**

**Capabilities:**
- Total budget tracking by facility
- Category-wise allocation:
  - Emergency preparedness
  - Staff resources
  - Equipment & supplies
  - Infrastructure
  - Research & development
  - Other expenses
- Risk-adjusted budget recommendations
- Period-based budget cycles
- Recommended reallocation strategies

**Technologies:**
- PostgreSQL for storage
- Financial algorithms
- Risk-based adjustments
- FastAPI for API layer

---

### 2. **Resource Allocation Intelligence**

**Capabilities:**
- Resource capacity tracking:
  - ICU beds
  - Ventilators
  - PPE supplies
  - Staff levels
  - Testing capacity
- Current vs. recommended capacity
- Utilization rate monitoring
- Priority level assignment (critical, high, medium, low)
- Risk-level correlation
- Allocation reasoning

**Technologies:**
- Real-time data processing
- Capacity optimization algorithms
- Alert generation for shortfalls

---

### 3. **AI-Powered Recommendations**

**Recommendation Types:**
1. **Operational Improvements**
   - Process optimization
   - Efficiency enhancements

2. **Financial Optimization**
   - Cost reduction strategies
   - Budget reallocation
   - ROI analysis

3. **Capacity Planning**
   - Resource scaling
   - Demand forecasting

4. **Risk Mitigation**
   - Preparedness strategies
   - Emergency planning

**Features:**
- Priority classification
- Estimated cost calculations
- Estimated savings projections
- Implementation timeframes
- Impact assessments

**Technologies:**
- ML-based pattern recognition
- Financial modeling
- Risk analysis algorithms
- Natural language generation for explanations

---

### 4. **Integrated Dashboard Analytics**

**Emory Hospital Dashboard Components:**

1. **Risk Overview**
   - Regional risk score display
   - Risk level badge
   - Risk probability percentage
   - Contributing factors

2. **Budget Overview**
   - Total, allocated, available budget
   - Risk-adjusted budget
   - Visual budget cards
   - Click-to-expand details

3. **Recommended Budget Adjustments**
   - Current vs. recommended per category
   - Adjustment reasons
   - Visual comparison
   - Category-wise breakdown

4. **Resource Allocation Grid**
   - Resource cards by type
   - Priority badges
   - Current/recommended capacity
   - Utilization bars
   - Color-coded status

5. **AI Recommendations Panel**
   - Recommendation cards
   - Priority and type badges
   - Impact descriptions
   - Financial metrics
   - Timeframe indicators

**Technologies:**
- React dashboard components
- Real-time data synchronization
- Interactive visualizations
- Modal dialogs for details

---

## Infrastructure & DevOps

### 1. **Docker Containerization**

**Containers:**
1. **Backend Container**
   - Python 3.11+
   - FastAPI application
   - All Python dependencies
   - Gunicorn/Uvicorn server

2. **Frontend Container**
   - Node.js build environment
   - Nginx web server
   - Optimized React build
   - Static asset serving

3. **Database Container**
   - PostgreSQL 15+
   - TimescaleDB extension
   - Persistent volume storage
   - Automated backups

**Technologies:**
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server and reverse proxy
- **Gunicorn** - Python WSGI HTTP server
- **Uvicorn** - ASGI server for async Python

**Files:**
- `docker-compose.yml` - Service orchestration
- `backend/Dockerfile` - Backend container definition
- `frontend/Dockerfile` - Frontend container definition
- `frontend/nginx.conf` - Nginx configuration

---

### 2. **Database Migrations**

**System:** Alembic

**Capabilities:**
- Version-controlled schema changes
- Automatic migration generation
- Rollback support
- Multi-environment support

**Migrations:**
- Initial schema creation
- Hospital insights tables
- Index additions
- Constraint modifications

**Technologies:**
- **Alembic** - Database migration tool
- SQLAlchemy integration
- PostgreSQL DDL

**Files:**
- `backend/alembic/` - Migration files
- `backend/alembic.ini` - Configuration
- `backend/alembic/env.py` - Environment setup

---

### 3. **Configuration Management**

**Environment Variables:**
- Database connection strings
- API keys (OpenRouter, etc.)
- Secret keys for security
- Feature flags
- Logging levels

**Technologies:**
- **python-dotenv** - Environment variable loading
- **Pydantic Settings** - Validated configuration
- `.env` files for local development
- Environment-specific configs

**File:**
- `backend/app/core/config.py` - Configuration management

---

### 4. **API Documentation**

**Automatic Documentation:**
- Interactive API explorer
- Request/response schemas
- Authentication requirements
- Example requests

**Technologies:**
- **FastAPI** - Auto-generates OpenAPI spec
- **Swagger UI** - Interactive documentation at `/docs`
- **ReDoc** - Alternative documentation at `/redoc`
- **Pydantic** - Schema generation

**Access:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 5. **Development Tools**

**Makefile Commands:**
- `make up` - Start all services
- `make down` - Stop all services
- `make migrate` - Run database migrations
- `make seed` - Seed database with data
- `make logs` - View container logs
- `make shell` - Access backend shell

**Scripts:**
- `run_app.sh` - Start application script
- `backend/render-build.sh` - Production build script
- Various utility scripts in `backend/scripts/`

---

## Technology Stack Summary

### Frontend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18+ | UI framework |
| TypeScript | 5+ | Type safety |
| Vite | 5+ | Build tool |
| Recharts | 2.5+ | Data visualization |
| Axios | 1.6+ | HTTP client |
| React Router | 6+ | Navigation |
| CSS3 | - | Styling |

### Backend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Programming language |
| FastAPI | 0.104+ | Web framework |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.12+ | Migrations |
| Pydantic | 2.5+ | Data validation |
| Uvicorn | 0.24+ | ASGI server |
| PostgreSQL | 15+ | Database |
| TimescaleDB | 2.11+ | Time-series extension |

### ML/AI Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Scikit-learn | 1.3+ | ML framework |
| XGBoost | 2.0+ | Gradient boosting |
| PyOD | 1.1+ | Anomaly detection |
| NumPy | 1.26+ | Numerical computing |
| Pandas | 2.1+ | Data manipulation |
| MLflow | 2.9+ | Experiment tracking |
| OpenRouter | API | LLM access |

### Data & ETL Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Prefect | 2.14+ | Workflow orchestration |
| PyTrends | 4.9+ | Google Trends API |
| HTTPX | 0.25+ | HTTP client |
| Requests | 2.31+ | HTTP library |

### Infrastructure Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Docker | 20+ | Containerization |
| Docker Compose | 2.0+ | Orchestration |
| Nginx | 1.24+ | Web server |
| PostgreSQL | 15+ | Database server |

### Optional/Future Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Snowflake | - | Analytics warehouse |
| Redis | 7+ | Caching |
| Celery | 5+ | Task queue |
| Grafana | 9+ | Monitoring |
| Prometheus | 2+ | Metrics |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │ Dashboard  │  │  Risk Map  │  │   Alerts & Hospital  │  │
│  └────────────┘  └────────────┘  └──────────────────────┘  │
│          React + TypeScript + Recharts                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST (Axios)
┌────────────────────────▼────────────────────────────────────┐
│                       BACKEND API                            │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌────────────┐  │
│  │  Health  │  │   Risk   │  │ Alerts  │  │  Hospital  │  │
│  │   API    │  │   API    │  │   API   │  │    API     │  │
│  └──────────┘  └──────────┘  └─────────┘  └────────────┘  │
│           FastAPI + SQLAlchemy + Pydantic                    │
└────────────┬───────────────┬──────────────┬────────────────┘
             │               │              │
        ┌────▼────┐     ┌────▼────┐   ┌────▼────┐
        │   ML    │     │   LLM   │   │   ETL   │
        │ Service │     │ Service │   │ Prefect │
        └────┬────┘     └────┬────┘   └────┬────┘
             │               │              │
             │         ┌─────▼──────┐       │
             │         │ OpenRouter │       │
             │         │    API     │       │
             │         └────────────┘       │
             │                              │
        ┌────▼──────────────────────────────▼────┐
        │     PostgreSQL + TimescaleDB            │
        │  ┌──────────┐  ┌────────────────────┐  │
        │  │   Time   │  │     Multi-Tenant   │  │
        │  │  Series  │  │        Data        │  │
        │  │   Data   │  │                    │  │
        │  └──────────┘  └────────────────────┘  │
        └─────────────────────────────────────────┘
```

---

## Data Flow

### 1. Data Ingestion Flow
```
External Sources → Prefect ETL → PostgreSQL → FastAPI → React
     (CDC,              (Process,     (Store)     (Serve)  (Display)
   Google Trends)       Transform)
```

### 2. Risk Assessment Flow
```
Health Metrics → ML Service → Risk Scores → Alert Generation → Dashboard
   (Database)    (Analyze)     (Store)      (Notify)           (Display)
```

### 3. User Query Flow
```
User Input → React → FastAPI → LLM Service → OpenRouter → Response
  (Type)    (Send)   (Route)   (Process)      (Reason)    (Display)
```

### 4. Hospital Intelligence Flow
```
Hospital Data → Recommendation Engine → AI Analysis → Dashboard
  (Metrics)          (Analyze)           (Generate)    (Present)
```

---

## Security Features

1. **Multi-Tenancy**
   - Data isolation by `tenant_id`
   - Row-level security (planned)
   - API-level filtering

2. **Input Validation**
   - Pydantic models for all inputs
   - Type checking
   - SQL injection prevention via ORM

3. **CORS Configuration**
   - Controlled origin access
   - Credential support

4. **Environment Variables**
   - Secret management
   - No hardcoded credentials

5. **Future Enhancements:**
   - JWT authentication
   - Role-based access control (RBAC)
   - API rate limiting
   - HTTPS enforcement

---

## Performance Optimizations

1. **Database**
   - Indexes on frequently queried fields
   - TimescaleDB hypertables
   - Connection pooling
   - Query optimization

2. **API**
   - Async/await patterns
   - Pagination for large datasets
   - Response caching (planned)
   - Lazy loading

3. **Frontend**
   - Code splitting
   - Lazy component loading
   - Memoization with React hooks
   - Optimized re-renders

4. **ETL**
   - Batch processing
   - Parallel task execution
   - Incremental updates

---

## Deployment Options

1. **Docker Compose** (Development/Small Scale)
   - Single command deployment
   - All services containerized
   - Easy local development

2. **Render** (Cloud Platform)
   - Automatic deployments
   - Managed PostgreSQL
   - Web service hosting

3. **Manual Deployment** (Production)
   - Separate service hosting
   - Load balancing
   - Database clustering
   - CDN for frontend

---

## Future Enhancements

### Planned Features
- [ ] Real-time websocket notifications
- [ ] Advanced geospatial visualization (Mapbox/Leaflet)
- [ ] Mobile responsive improvements
- [ ] User authentication & authorization
- [ ] Multi-language support
- [ ] Export functionality (PDF/CSV reports)
- [ ] Email/SMS alert notifications
- [ ] Advanced ML model training UI
- [ ] Integration with more public health APIs
- [ ] Snowflake data warehouse integration
- [ ] BI tool connectors (Tableau, PowerBI)
- [ ] GraphQL API option
- [ ] Automated testing suite
- [ ] Performance monitoring dashboard

### Technology Additions
- Redis for caching
- Celery for background tasks
- Grafana for monitoring
- Prometheus for metrics
- Jest/Pytest for testing
- GitHub Actions for CI/CD

---

## Getting Help

- **Documentation:** See `README.md`, `SETUP.md`, `TECH_STACK.md`
- **API Docs:** http://localhost:8000/docs
- **Issues:** Check project issues on GitHub
- **Contributing:** See `CONTRIBUTING.md` (if exists)

---

## License

[Your License Here]

---

**Last Updated:** November 2024
**Version:** 1.0.0

