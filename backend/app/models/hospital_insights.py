"""
Hospital insights and recommendations models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class HospitalBudget(Base):
    """Hospital budget allocations and recommendations"""
    __tablename__ = "hospital_budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    facility_id = Column(String, nullable=False, index=True)
    facility_name = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Budget categories
    total_budget = Column(Float, nullable=False)
    allocated_budget = Column(Float, nullable=False)
    available_budget = Column(Float, nullable=False)
    
    # Budget breakdown by category
    emergency_preparedness = Column(Float, nullable=False, default=0.0)
    staff_resources = Column(Float, nullable=False, default=0.0)
    equipment_supplies = Column(Float, nullable=False, default=0.0)
    infrastructure = Column(Float, nullable=False, default=0.0)
    research_development = Column(Float, nullable=False, default=0.0)
    other = Column(Float, nullable=False, default=0.0)
    
    # Recommendations
    recommended_allocation = Column(JSON, nullable=True)  # JSON with category recommendations
    risk_adjusted_budget = Column(Float, nullable=True)  # Budget adjusted for current risk level
    
    currency = Column(String, nullable=False, default="USD")
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ResourceAllocation(Base):
    """Resource allocation recommendations for hospitals"""
    __tablename__ = "resource_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    facility_id = Column(String, nullable=False, index=True)
    facility_name = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Resource categories
    resource_type = Column(String, nullable=False)  # 'staff', 'equipment', 'supplies', 'beds', 'medication'
    current_capacity = Column(Float, nullable=False)
    recommended_capacity = Column(Float, nullable=False)
    utilization_rate = Column(Float, nullable=False)  # Percentage
    
    # Allocation details
    current_allocation = Column(Float, nullable=False)
    recommended_allocation = Column(Float, nullable=False)
    allocation_reason = Column(Text, nullable=True)
    priority_level = Column(String, nullable=False)  # 'critical', 'high', 'medium', 'low'
    
    # Risk context
    risk_score_id = Column(Integer, ForeignKey("risk_scores.id"), nullable=True)
    risk_level = Column(String, nullable=True)
    
    status = Column(String, nullable=False, default="recommended")  # 'recommended', 'approved', 'implemented'
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HospitalRecommendation(Base):
    """AI-generated recommendations for hospitals"""
    __tablename__ = "hospital_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    facility_id = Column(String, nullable=False, index=True)
    facility_name = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Recommendation details
    recommendation_type = Column(String, nullable=False)  # 'budget', 'resource', 'operational', 'preparedness'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, nullable=False)  # 'critical', 'high', 'medium', 'low'
    
    # Impact and metrics
    estimated_impact = Column(String, nullable=True)  # e.g., "Reduce costs by 15%", "Increase capacity by 20%"
    estimated_cost = Column(Float, nullable=True)
    estimated_savings = Column(Float, nullable=True)
    
    # Implementation
    implementation_steps = Column(JSON, nullable=True)  # Array of steps
    timeframe = Column(String, nullable=True)  # e.g., "2 weeks", "1 month"
    status = Column(String, nullable=False, default="pending")  # 'pending', 'in_progress', 'completed', 'dismissed'
    
    # Context
    risk_score_id = Column(Integer, ForeignKey("risk_scores.id"), nullable=True)
    related_metrics = Column(JSON, nullable=True)  # Related health metrics that influenced this recommendation
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

