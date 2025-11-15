"""
Risk scores API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.risk_scores import RiskScore, Anomaly
from pydantic import BaseModel

router = APIRouter()


class RiskScoreResponse(BaseModel):
    id: int
    region_id: str
    timestamp: datetime
    risk_probability: float
    risk_level: str
    contributing_factors: Optional[str] = None


@router.get("/scores")
async def get_risk_scores(
    region_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[int] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get outbreak risk scores by region"""
    query = db.query(RiskScore)
    
    if tenant_id:
        query = query.filter(RiskScore.tenant_id == tenant_id)
    if region_id:
        query = query.filter(RiskScore.region_id == region_id)
    if start_date:
        query = query.filter(RiskScore.timestamp >= start_date)
    if end_date:
        query = query.filter(RiskScore.timestamp <= end_date)
    
    scores = query.order_by(RiskScore.timestamp.desc()).limit(limit).all()
    
    return {
        "scores": [
            {
                "id": s.id,
                "region_id": s.region_id,
                "timestamp": s.timestamp.isoformat(),
                "risk_probability": s.risk_probability,
                "risk_level": s.risk_level,
                "contributing_factors": s.contributing_factors
            }
            for s in scores
        ]
    }


@router.get("/scores/latest")
async def get_latest_risk_scores(
    tenant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get latest risk scores for all regions"""
    # Get the most recent timestamp
    latest_query = db.query(func.max(RiskScore.timestamp))
    if tenant_id:
        latest_query = latest_query.filter(RiskScore.tenant_id == tenant_id)
    latest_timestamp = latest_query.scalar()
    
    if not latest_timestamp:
        return {"scores": []}
    
    # Get all scores at that timestamp
    query = db.query(RiskScore).filter(RiskScore.timestamp == latest_timestamp)
    if tenant_id:
        query = query.filter(RiskScore.tenant_id == tenant_id)
    
    scores = query.all()
    
    return {
        "timestamp": latest_timestamp.isoformat() if latest_timestamp else None,
        "scores": [
            {
                "id": s.id,
                "region_id": s.region_id,
                "risk_probability": s.risk_probability,
                "risk_level": s.risk_level,
                "contributing_factors": s.contributing_factors
            }
            for s in scores
        ]
    }


@router.get("/anomalies")
async def get_anomalies(
    region_id: Optional[str] = Query(None),
    metric_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[int] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get detected anomalies"""
    query = db.query(Anomaly).filter(Anomaly.is_anomaly == True)
    
    if tenant_id:
        query = query.filter(Anomaly.tenant_id == tenant_id)
    if region_id:
        query = query.filter(Anomaly.region_id == region_id)
    if metric_type:
        query = query.filter(Anomaly.metric_type == metric_type)
    if start_date:
        query = query.filter(Anomaly.timestamp >= start_date)
    if end_date:
        query = query.filter(Anomaly.timestamp <= end_date)
    
    anomalies = query.order_by(Anomaly.timestamp.desc()).limit(limit).all()
    
    return {
        "anomalies": [
            {
                "id": a.id,
                "region_id": a.region_id,
                "metric_type": a.metric_type,
                "metric_value": a.metric_value,
                "anomaly_score": a.anomaly_score,
                "description": a.description,
                "timestamp": a.timestamp.isoformat()
            }
            for a in anomalies
        ]
    }

