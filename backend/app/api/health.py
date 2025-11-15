"""
Health metrics API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.models.health_metrics import SearchTrend, PharmacyAggregate, HospitalUtilization, OWIDCovidMetric
from pydantic import BaseModel

router = APIRouter()


class HealthMetricResponse(BaseModel):
    region_id: str
    timestamp: datetime
    value: float
    metric_type: str


class SearchTrendResponse(BaseModel):
    region_id: str
    keyword: str
    timestamp: datetime
    search_index: float


@router.get("/metrics")
async def get_health_metrics(
    region_id: Optional[str] = Query(None),
    metric_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get health metrics aggregated by region and time"""
    # Default to last 30 days if no dates provided
    if not end_date:
        end_date = datetime.now(timezone.utc)
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # This is a simplified endpoint - in production, you'd aggregate across different metric types
    return {
        "region_id": region_id,
        "start_date": start_date,
        "end_date": end_date,
        "metrics": []
    }


@router.get("/search-trends")
async def get_search_trends(
    region_id: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get search trend metrics"""
    query = db.query(SearchTrend)
    
    if tenant_id:
        query = query.filter(SearchTrend.tenant_id == tenant_id)
    if region_id:
        query = query.filter(SearchTrend.region_id == region_id)
    if keyword:
        query = query.filter(SearchTrend.keyword == keyword)
    if start_date:
        query = query.filter(SearchTrend.timestamp >= start_date)
    if end_date:
        query = query.filter(SearchTrend.timestamp <= end_date)
    
    trends = query.order_by(SearchTrend.timestamp.desc()).limit(1000).all()
    
    return {
        "trends": [
            {
                "region_id": t.region_id,
                "keyword": t.keyword,
                "timestamp": t.timestamp.isoformat(),
                "search_index": t.search_index
            }
            for t in trends
        ]
    }


@router.get("/pharmacy")
async def get_pharmacy_metrics(
    region_id: Optional[str] = Query(None),
    drug_category: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get pharmacy aggregate metrics"""
    query = db.query(PharmacyAggregate)
    
    if tenant_id:
        query = query.filter(PharmacyAggregate.tenant_id == tenant_id)
    if region_id:
        query = query.filter(PharmacyAggregate.region_id == region_id)
    if drug_category:
        query = query.filter(PharmacyAggregate.drug_category == drug_category)
    if start_date:
        query = query.filter(PharmacyAggregate.timestamp >= start_date)
    if end_date:
        query = query.filter(PharmacyAggregate.timestamp <= end_date)
    
    metrics = query.order_by(PharmacyAggregate.timestamp.desc()).limit(1000).all()
    
    return {
        "metrics": [
            {
                "region_id": m.region_id,
                "drug_category": m.drug_category,
                "timestamp": m.timestamp.isoformat(),
                "count": m.count
            }
            for m in metrics
        ]
    }


@router.get("/hospital-utilization")
async def get_hospital_utilization(
    region_id: Optional[str] = Query(None),
    facility_id: Optional[str] = Query(None),
    metric_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get hospital utilization metrics"""
    query = db.query(HospitalUtilization)
    
    if tenant_id:
        query = query.filter(HospitalUtilization.tenant_id == tenant_id)
    if region_id:
        query = query.filter(HospitalUtilization.region_id == region_id)
    if facility_id:
        query = query.filter(HospitalUtilization.facility_id == facility_id)
    if metric_type:
        query = query.filter(HospitalUtilization.metric_type == metric_type)
    if start_date:
        query = query.filter(HospitalUtilization.timestamp >= start_date)
    if end_date:
        query = query.filter(HospitalUtilization.timestamp <= end_date)
    
    metrics = query.order_by(HospitalUtilization.timestamp.desc()).limit(1000).all()
    
    return {
        "metrics": [
            {
                "region_id": m.region_id,
                "facility_id": m.facility_id,
                "metric_type": m.metric_type,
                "value": m.value,
                "unit": m.unit,
                "timestamp": m.timestamp.isoformat()
            }
            for m in metrics
        ]
    }

