"""
FinTech simulation models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class FundAllocation(Base):
    """Simulated fund allocations based on risk"""
    __tablename__ = "fund_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    region_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    risk_score_id = Column(Integer, ForeignKey("risk_scores.id"), nullable=True)
    allocated_amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    allocation_reason = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="simulated")  # 'simulated', 'pending', 'executed'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

