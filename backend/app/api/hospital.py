"""
Hospital insights and recommendations API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.models.hospital_insights import HospitalBudget, ResourceAllocation, HospitalRecommendation
from app.models.risk_scores import RiskScore
from pydantic import BaseModel

router = APIRouter()


class HospitalBudgetResponse(BaseModel):
    id: int
    facility_id: str
    facility_name: str
    timestamp: datetime
    total_budget: float
    allocated_budget: float
    available_budget: float
    emergency_preparedness: float
    staff_resources: float
    equipment_supplies: float
    infrastructure: float
    research_development: float
    other: float
    recommended_allocation: Optional[dict] = None
    risk_adjusted_budget: Optional[float] = None
    currency: str
    period_start: datetime
    period_end: datetime


class ResourceAllocationResponse(BaseModel):
    id: int
    facility_id: str
    facility_name: str
    timestamp: datetime
    resource_type: str
    current_capacity: float
    recommended_capacity: float
    utilization_rate: float
    current_allocation: float
    recommended_allocation: float
    allocation_reason: Optional[str] = None
    priority_level: str
    risk_level: Optional[str] = None
    status: str


class HospitalRecommendationResponse(BaseModel):
    id: int
    facility_id: str
    facility_name: str
    timestamp: datetime
    recommendation_type: str
    title: str
    description: str
    priority: str
    estimated_impact: Optional[str] = None
    estimated_cost: Optional[float] = None
    estimated_savings: Optional[float] = None
    implementation_steps: Optional[List[str]] = None
    timeframe: Optional[str] = None
    status: str


@router.get("/budgets")
async def get_hospital_budgets(
    facility_id: Optional[str] = Query(None),
    tenant_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get hospital budget data"""
    query = db.query(HospitalBudget)
    
    if tenant_id:
        query = query.filter(HospitalBudget.tenant_id == tenant_id)
    if facility_id:
        query = query.filter(HospitalBudget.facility_id == facility_id)
    if start_date:
        query = query.filter(HospitalBudget.timestamp >= start_date)
    if end_date:
        query = query.filter(HospitalBudget.timestamp <= end_date)
    
    budgets = query.order_by(HospitalBudget.timestamp.desc()).limit(limit).all()
    
    return {
        "budgets": [
            {
                "id": b.id,
                "facility_id": b.facility_id,
                "facility_name": b.facility_name,
                "timestamp": b.timestamp.isoformat(),
                "total_budget": b.total_budget,
                "allocated_budget": b.allocated_budget,
                "available_budget": b.available_budget,
                "emergency_preparedness": b.emergency_preparedness,
                "staff_resources": b.staff_resources,
                "equipment_supplies": b.equipment_supplies,
                "infrastructure": b.infrastructure,
                "research_development": b.research_development,
                "other": b.other,
                "recommended_allocation": b.recommended_allocation,
                "risk_adjusted_budget": b.risk_adjusted_budget,
                "currency": b.currency,
                "period_start": b.period_start.isoformat(),
                "period_end": b.period_end.isoformat()
            }
            for b in budgets
        ]
    }


@router.get("/budgets/latest")
async def get_latest_hospital_budget(
    facility_id: str = Query(..., description="Facility ID (e.g., 'emory-main')"),
    tenant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get the latest budget for a specific hospital"""
    query = db.query(HospitalBudget).filter(HospitalBudget.facility_id == facility_id)
    
    if tenant_id:
        query = query.filter(HospitalBudget.tenant_id == tenant_id)
    
    budget = query.order_by(HospitalBudget.timestamp.desc()).first()
    
    if not budget:
        return {"error": "No budget data found for this facility"}
    
    return {
        "id": budget.id,
        "facility_id": budget.facility_id,
        "facility_name": budget.facility_name,
        "timestamp": budget.timestamp.isoformat(),
        "total_budget": budget.total_budget,
        "allocated_budget": budget.allocated_budget,
        "available_budget": budget.available_budget,
        "emergency_preparedness": budget.emergency_preparedness,
        "staff_resources": budget.staff_resources,
        "equipment_supplies": budget.equipment_supplies,
        "infrastructure": budget.infrastructure,
        "research_development": budget.research_development,
        "other": budget.other,
        "recommended_allocation": budget.recommended_allocation,
        "risk_adjusted_budget": budget.risk_adjusted_budget,
        "currency": budget.currency,
        "period_start": budget.period_start.isoformat(),
        "period_end": budget.period_end.isoformat()
    }


@router.get("/resource-allocations")
async def get_resource_allocations(
    facility_id: Optional[str] = Query(None),
    tenant_id: Optional[int] = Query(None),
    resource_type: Optional[str] = Query(None),
    priority_level: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get resource allocation recommendations"""
    query = db.query(ResourceAllocation)
    
    if tenant_id:
        query = query.filter(ResourceAllocation.tenant_id == tenant_id)
    if facility_id:
        query = query.filter(ResourceAllocation.facility_id == facility_id)
    if resource_type:
        query = query.filter(ResourceAllocation.resource_type == resource_type)
    if priority_level:
        query = query.filter(ResourceAllocation.priority_level == priority_level)
    if start_date:
        query = query.filter(ResourceAllocation.timestamp >= start_date)
    if end_date:
        query = query.filter(ResourceAllocation.timestamp <= end_date)
    
    allocations = query.order_by(ResourceAllocation.timestamp.desc()).limit(limit).all()
    
    return {
        "allocations": [
            {
                "id": a.id,
                "facility_id": a.facility_id,
                "facility_name": a.facility_name,
                "timestamp": a.timestamp.isoformat(),
                "resource_type": a.resource_type,
                "current_capacity": a.current_capacity,
                "recommended_capacity": a.recommended_capacity,
                "utilization_rate": a.utilization_rate,
                "current_allocation": a.current_allocation,
                "recommended_allocation": a.recommended_allocation,
                "allocation_reason": a.allocation_reason,
                "priority_level": a.priority_level,
                "risk_level": a.risk_level,
                "status": a.status
            }
            for a in allocations
        ]
    }


@router.get("/recommendations")
async def get_hospital_recommendations(
    facility_id: Optional[str] = Query(None),
    tenant_id: Optional[int] = Query(None),
    recommendation_type: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Get AI-generated hospital recommendations"""
    query = db.query(HospitalRecommendation)
    
    if tenant_id:
        query = query.filter(HospitalRecommendation.tenant_id == tenant_id)
    if facility_id:
        query = query.filter(HospitalRecommendation.facility_id == facility_id)
    if recommendation_type:
        query = query.filter(HospitalRecommendation.recommendation_type == recommendation_type)
    if priority:
        query = query.filter(HospitalRecommendation.priority == priority)
    if status:
        query = query.filter(HospitalRecommendation.status == status)
    if start_date:
        query = query.filter(HospitalRecommendation.timestamp >= start_date)
    if end_date:
        query = query.filter(HospitalRecommendation.timestamp <= end_date)
    
    recommendations = query.order_by(HospitalRecommendation.timestamp.desc()).limit(limit).all()
    
    return {
        "recommendations": [
            {
                "id": r.id,
                "facility_id": r.facility_id,
                "facility_name": r.facility_name,
                "timestamp": r.timestamp.isoformat(),
                "recommendation_type": r.recommendation_type,
                "title": r.title,
                "description": r.description,
                "priority": r.priority,
                "estimated_impact": r.estimated_impact,
                "estimated_cost": r.estimated_cost,
                "estimated_savings": r.estimated_savings,
                "implementation_steps": r.implementation_steps,
                "timeframe": r.timeframe,
                "status": r.status
            }
            for r in recommendations
        ]
    }


@router.get("/dashboard")
async def get_hospital_dashboard(
    facility_id: str = Query(..., description="Facility ID (e.g., 'emory-main')"),
    tenant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard data for a hospital"""
    # Get latest budget
    budget_query = db.query(HospitalBudget).filter(HospitalBudget.facility_id == facility_id)
    if tenant_id:
        budget_query = budget_query.filter(HospitalBudget.tenant_id == tenant_id)
    latest_budget = budget_query.order_by(HospitalBudget.timestamp.desc()).first()
    
    # Get latest risk score for the region
    facility_name = latest_budget.facility_name if latest_budget else "Unknown"
    region_id = "US-GA"  # Emory is in Georgia
    
    risk_query = db.query(RiskScore).filter(RiskScore.region_id == region_id)
    if tenant_id:
        risk_query = risk_query.filter(RiskScore.tenant_id == tenant_id)
    latest_risk = risk_query.order_by(RiskScore.timestamp.desc()).first()
    
    # Get active resource allocations
    allocation_query = db.query(ResourceAllocation).filter(
        ResourceAllocation.facility_id == facility_id,
        ResourceAllocation.status.in_(['recommended', 'approved'])
    )
    if tenant_id:
        allocation_query = allocation_query.filter(ResourceAllocation.tenant_id == tenant_id)
    active_allocations = allocation_query.order_by(ResourceAllocation.priority_level.desc()).limit(10).all()
    
    # Get active recommendations
    rec_query = db.query(HospitalRecommendation).filter(
        HospitalRecommendation.facility_id == facility_id,
        HospitalRecommendation.status.in_(['pending', 'in_progress'])
    )
    if tenant_id:
        rec_query = rec_query.filter(HospitalRecommendation.tenant_id == tenant_id)
    active_recommendations = rec_query.order_by(HospitalRecommendation.priority.desc()).limit(10).all()
    
    return {
        "facility_id": facility_id,
        "facility_name": facility_name,
        "region_id": region_id,
        "budget": {
            "id": latest_budget.id,
            "total_budget": latest_budget.total_budget,
            "allocated_budget": latest_budget.allocated_budget,
            "available_budget": latest_budget.available_budget,
            "risk_adjusted_budget": latest_budget.risk_adjusted_budget,
            "recommended_allocation": latest_budget.recommended_allocation,
            "timestamp": latest_budget.timestamp.isoformat()
        } if latest_budget else None,
        "risk_score": {
            "risk_level": latest_risk.risk_level,
            "risk_probability": latest_risk.risk_probability,
            "contributing_factors": latest_risk.contributing_factors,
            "timestamp": latest_risk.timestamp.isoformat()
        } if latest_risk else None,
        "resource_allocations": [
            {
                "id": a.id,
                "resource_type": a.resource_type,
                "current_capacity": a.current_capacity,
                "recommended_capacity": a.recommended_capacity,
                "utilization_rate": a.utilization_rate,
                "priority_level": a.priority_level,
                "allocation_reason": a.allocation_reason
            }
            for a in active_allocations
        ],
        "recommendations": [
            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "priority": r.priority,
                "recommendation_type": r.recommendation_type,
                "estimated_impact": r.estimated_impact,
                "estimated_cost": r.estimated_cost,
                "estimated_savings": r.estimated_savings,
                "timeframe": r.timeframe
            }
            for r in active_recommendations
        ]
    }

