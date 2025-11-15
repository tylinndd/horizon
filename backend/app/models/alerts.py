"""
Alert models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Alert(Base):
    """System alerts for outbreaks and anomalies"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    region_id = Column(String, nullable=False, index=True)
    alert_type = Column(String, nullable=False)  # 'outbreak', 'anomaly', 'risk_increase'
    severity = Column(String, nullable=False)  # 'low', 'medium', 'high', 'critical'
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    risk_score_id = Column(Integer, ForeignKey("risk_scores.id"), nullable=True)
    anomaly_id = Column(Integer, ForeignKey("anomalies.id"), nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)
    is_acknowledged = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)

