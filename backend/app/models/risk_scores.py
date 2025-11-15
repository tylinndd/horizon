"""
Risk scores and anomaly detection models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.core.database import Base


class RiskScore(Base):
    """Outbreak risk scores by region"""
    __tablename__ = "risk_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    region_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    risk_probability = Column(Float, nullable=False)  # 0.0 to 1.0
    risk_level = Column(String, nullable=False)  # 'low', 'medium', 'high', 'critical'
    contributing_factors = Column(Text, nullable=True)  # JSON string of factors
    model_version = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Anomaly(Base):
    """Detected anomalies in health indicators"""
    __tablename__ = "anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    region_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    metric_type = Column(String, nullable=False)  # e.g., 'pharmacy', 'search_trend', 'hospital_utilization'
    metric_value = Column(Float, nullable=False)
    anomaly_score = Column(Float, nullable=False)  # 0.0 to 1.0
    is_anomaly = Column(Boolean, nullable=False, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

