# Horizon Data Sources

## Current Data Status

Your Horizon platform uses **realistic simulated data** that mirrors real-world outbreak patterns and trends.

## Why Simulated Data?

1. **Privacy & Compliance**: Real patient data requires HIPAA compliance, extensive legal agreements, and data use authorization
2. **Consistency**: Simulated data provides reliable testing without API rate limits or outages
3. **Realism**: Our algorithms incorporate actual epidemiological patterns and seasonal trends

## Data Components

### 1. Risk Scores (Realistic Simulation)
- **Source**: Algorithmic generation based on real epidemiological patterns
- **Update Frequency**: Real-time (every time you run `make update-data`)
- **Regions Covered**: US states (California, New York, Texas, Florida, Illinois)
- **Parameters**:
  - Risk probability (0-100%)
  - Risk levels (low, medium, high, critical)
  - Contributing factors (illness type, trend direction, hospital pressure)

### 2. Search Trends (Google Trends Pattern)
- **Simulated from**: Google Trends API methodology
- **Keywords**: fever, cough, flu symptoms, COVID symptoms, shortness of breath, body aches
- **Realism Features**:
  - Seasonal variations
  - Regional differences
  - Correlated with outbreak intensity

### 3. Pharmacy Data (CVS/Walgreens Pattern)
- **Simulated from**: Retail pharmacy purchase patterns
- **Drug Categories**:
  - Antipyretics (fever reducers)
  - Cough suppressants
  - Antivirals
  - Decongestants
  - Pain relievers
- **Realism**: Purchase volumes scaled by outbreak severity

### 4. Hospital Metrics (CDC Pattern)
- **Simulated from**: CDC hospital utilization reporting
- **Metrics**:
  - Bed occupancy rates
  - ICU usage
  - Emergency room visits
  - PPE usage rates
- **Ranges**: 30-95% (realistic hospital operating ranges)

## Current Outbreak Scenarios

Your platform displays these realistic scenarios:

### 🔴 US-CA (California) - High Risk, Increasing
- **Primary Illness**: Respiratory syncytial virus (RSV)
- **Trend**: Increasing
- **Hospital Pressure**: 72%

### 🔴 US-TX (Texas) - Critical Risk, Increasing
- **Primary Illness**: COVID-19 variant
- **Trend**: Increasing
- **Hospital Pressure**: 68%

### 🟡 US-NY (New York) - Medium Risk, Stable
- **Primary Illness**: Seasonal influenza
- **Trend**: Stable
- **Hospital Pressure**: 65%

### 🟡 US-FL (Florida) - Medium Risk, Decreasing
- **Primary Illness**: Dengue fever
- **Trend**: Decreasing
- **Hospital Pressure**: 58%

### 🟢 US-IL (Illinois) - Medium Risk, Stable
- **Primary Illness**: Influenza A
- **Trend**: Stable
- **Hospital Pressure**: 61%

## Real Data Integration (Available)

The platform **can** integrate real data from these sources:

### ✅ Our World in Data (OWID)
- **URL**: https://covid.ourworldindata.org/
- **Data**: COVID-19 cases, deaths, hospitalizations, testing
- **Coverage**: Global
- **Update**: Daily
- **Status**: API integration ready (`backend/app/etl/flows.py`)

### ✅ Google Trends
- **Library**: `pytrends`
- **Data**: Search interest over time for health symptoms
- **Coverage**: Regional search data
- **Status**: Integration code ready

### ✅ CDC APIs (Future)
- **Potential Sources**:
  - FluView (influenza surveillance)
  - NSSP (syndromic surveillance)
  - Hospital capacity data
- **Status**: Would require API access approval

## How to Update Data

### Manual Update (Run Anytime)
```bash
make update-data
```

This runs the realistic data pipeline and refreshes all metrics.

### Automatic Real-Time Integration

To switch to **real data sources** (requires network access and API setup):

1. **Enable OWID Integration**:
```bash
cd backend
source venv/bin/activate
python -c "from app.etl.flows import ingest_public_data_flow; ingest_public_data_flow()"
```

2. **Set up Google Trends** (requires pytrends configuration):
```python
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)
```

3. **Schedule automatic updates** with cron or Prefect Cloud

## Data Quality & Validation

All data (real or simulated) goes through:
- ✅ Range validation (no impossible values)
- ✅ Temporal consistency checks
- ✅ Cross-metric correlation validation
- ✅ Anomaly detection algorithms

## For Production Use

To move Horizon to production with real data:

1. **Obtain necessary data access**:
   - CDC Data Use Agreement
   - Google Trends API setup
   - Hospital data partnerships

2. **Enable ETL pipelines**:
   - Uncomment real data flows in `backend/app/etl/flows.py`
   - Configure API keys in `.env`
   - Set up Prefect scheduling

3. **Compliance**:
   - HIPAA compliance review
   - Data privacy audit
   - Security assessment

## Summary

**Current Status**: Realistic simulated data based on actual epidemiological patterns

**Capability**: Ready to integrate real data from OWID, Google Trends, and CDC APIs

**Quality**: Scientifically informed algorithms producing realistic outbreak scenarios

**Purpose**: Demonstration of outbreak detection capabilities without requiring sensitive real-time patient data

---

*Last updated: November 15, 2025*

