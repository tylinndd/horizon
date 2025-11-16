# Emory Hospital Integration Guide

This document describes the Emory Hospital integration with the Horizon platform, including mock data generation and dashboard access.

## Overview

The Emory Hospital integration simulates a real hospital system connected to Horizon, providing:
- **Budget Management**: Quarterly budget allocations with risk-adjusted recommendations
- **Resource Allocation**: AI-powered recommendations for staff, equipment, supplies, beds, and medications
- **Operational Recommendations**: Actionable insights for improving hospital operations
- **Risk-Based Insights**: All recommendations are adjusted based on current regional risk levels

## Setup Instructions

### 1. Run Database Migration

First, apply the database migration to create the new tables:

```bash
cd backend
alembic upgrade head
```

### 2. Generate Mock Data

Run the script to generate Emory Hospital mock data:

```bash
cd backend
python scripts/generate_emory_hospital_data.py
```

This will create:
- Budget data for the current and past quarters
- Resource allocation recommendations
- AI-powered operational recommendations

### 3. Access the Dashboard

Once the data is generated, access the Emory Hospital dashboard at:

```
http://localhost:3000/hospital/emory
```

## Data Structure

### Hospital Budget
- **Total Budget**: $625M per quarter (based on $2.5B annual budget)
- **Categories**: Emergency Preparedness, Staff Resources, Equipment & Supplies, Infrastructure, Research & Development, Other
- **Risk Adjustment**: Budget recommendations adjust based on current regional risk level (Georgia - US-GA)

### Resource Allocations
- **Staff**: Current capacity, recommended capacity, utilization rates
- **Equipment**: Ventilators, ICU beds, critical care equipment
- **Supplies**: PPE, medical supplies inventory
- **Beds**: Total bed capacity and utilization
- **Medication**: Critical medication stockpiles

### Recommendations
- **Budget**: Recommendations for budget reallocation
- **Resource**: Staffing and equipment optimization
- **Operational**: Process improvements and efficiency gains
- **Preparedness**: Outbreak response and surge capacity planning

## API Endpoints

### Get Hospital Dashboard
```
GET /api/hospital/dashboard?facility_id=emory-main&tenant_id=1
```

Returns comprehensive dashboard data including budget, risk scores, resource allocations, and recommendations.

### Get Budget Data
```
GET /api/hospital/budgets?facility_id=emory-main&tenant_id=1
GET /api/hospital/budgets/latest?facility_id=emory-main&tenant_id=1
```

### Get Resource Allocations
```
GET /api/hospital/resource-allocations?facility_id=emory-main&tenant_id=1
```

### Get Recommendations
```
GET /api/hospital/recommendations?facility_id=emory-main&tenant_id=1
```

## Configuration

### Emory Hospital Constants
- **Tenant ID**: 1
- **Facility ID**: `emory-main`
- **Facility Name**: `Emory University Hospital`
- **Region**: `US-GA` (Georgia)
- **Annual Budget**: $2.5 billion

These can be modified in `backend/scripts/generate_emory_hospital_data.py`.

## Features

### Risk-Based Adjustments
All recommendations and budget allocations are dynamically adjusted based on the current risk level in Georgia:
- **Low Risk** (< 0.35): Standard allocations
- **Medium Risk** (0.35-0.54): Moderate increases
- **High Risk** (0.55-0.74): Significant increases
- **Critical Risk** (> 0.75): Maximum preparedness allocations

### Real-Time Updates
The dashboard refreshes every 5 minutes to show the latest data. Risk scores are pulled from the regional risk assessment system.

## Example Recommendations

1. **Increase Emergency Preparedness Budget**: Adjusts budget allocation based on current risk level
2. **Optimize Staffing Levels**: Recommendations for hiring and on-call pools
3. **Predictive Analytics**: Deploy AI models for resource planning
4. **ICU Capacity Enhancement**: Increase critical care capacity
5. **Supply Chain Optimization**: Improve inventory management
6. **Telemedicine Infrastructure**: Expand virtual care capabilities

## Integration Points

The Emory Hospital integration connects to:
- **Risk Assessment System**: Pulls regional risk scores for Georgia
- **Health Metrics**: Uses hospital utilization metrics
- **Alert System**: Can trigger alerts based on resource constraints
- **Financial Planning**: Provides budget recommendations based on risk

## Next Steps

To extend this integration:
1. Add more facilities (e.g., Emory Midtown, Emory Decatur)
2. Integrate real-time EMR data
3. Add predictive modeling for patient volumes
4. Connect to actual hospital financial systems
5. Implement recommendation approval workflows

