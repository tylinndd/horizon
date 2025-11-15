"""
Alerts API endpoints
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.alerts import Alert
from pydantic import BaseModel

router = APIRouter()


class AlertResponse(BaseModel):
    id: int
    region_id: str
    alert_type: str
    severity: str
    title: str
    message: str
    is_read: bool
    is_acknowledged: bool
    created_at: datetime


@router.get("")
async def get_alerts(
    region_id: Optional[str] = Query(None),
    alert_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    is_read: Optional[bool] = Query(None),
    tenant_id: Optional[int] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get alerts"""
    query = db.query(Alert)
    
    if tenant_id:
        query = query.filter(Alert.tenant_id == tenant_id)
    if region_id:
        query = query.filter(Alert.region_id == region_id)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    if severity:
        query = query.filter(Alert.severity == severity)
    if is_read is not None:
        query = query.filter(Alert.is_read == is_read)
    
    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    
    return {
        "alerts": [
            {
                "id": a.id,
                "region_id": a.region_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "title": a.title,
                "message": a.message,
                "is_read": a.is_read,
                "is_acknowledged": a.is_acknowledged,
                "created_at": a.created_at.isoformat()
            }
            for a in alerts
        ]
    }


@router.patch("/{alert_id}/read")
async def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Mark an alert as read"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_read = True
    db.commit()
    
    return {"message": "Alert marked as read", "alert_id": alert_id}


@router.patch("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Acknowledge an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_acknowledged = True
    alert.acknowledged_at = datetime.now(timezone.utc)
    db.commit()
    
    return {"message": "Alert acknowledged", "alert_id": alert_id}

