"""
FinTech simulation API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.fintech import FundAllocation
from pydantic import BaseModel

router = APIRouter()


class FundAllocationResponse(BaseModel):
    id: int
    region_id: str
    timestamp: datetime
    allocated_amount: float
    currency: str
    allocation_reason: Optional[str] = None
    status: str


@router.get("/allocations")
async def get_fund_allocations(
    region_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tenant_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get fund allocations"""
    query = db.query(FundAllocation)
    
    if tenant_id:
        query = query.filter(FundAllocation.tenant_id == tenant_id)
    if region_id:
        query = query.filter(FundAllocation.region_id == region_id)
    if status:
        query = query.filter(FundAllocation.status == status)
    if start_date:
        query = query.filter(FundAllocation.timestamp >= start_date)
    if end_date:
        query = query.filter(FundAllocation.timestamp <= end_date)
    
    allocations = query.order_by(FundAllocation.timestamp.desc()).limit(limit).all()
    
    return {
        "allocations": [
            {
                "id": a.id,
                "region_id": a.region_id,
                "timestamp": a.timestamp.isoformat(),
                "allocated_amount": a.allocated_amount,
                "currency": a.currency,
                "allocation_reason": a.allocation_reason,
                "status": a.status
            }
            for a in allocations
        ]
    }

