"""
Health metrics database models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base


class HealthMetric(Base):
    """Base health metric with common fields"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, index=True)  # Multi-tenant support
    region_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SearchTrend(HealthMetric):
    """Search trends from Google Trends"""
    __tablename__ = "search_trends_metrics"
    
    keyword = Column(String, nullable=False, index=True)
    search_index = Column(Float, nullable=False)  # Relative search interest


class PharmacyAggregate(HealthMetric):
    """Pharmacy medication aggregates"""
    __tablename__ = "pharmacy_aggregates"
    
    drug_category = Column(String, nullable=False, index=True)
    count = Column(Integer, nullable=False)


class HospitalUtilization(HealthMetric):
    """Hospital utilization metrics"""
    __tablename__ = "hospital_utilization_metrics"
    
    facility_id = Column(String, nullable=True, index=True)
    metric_type = Column(String, nullable=False)  # e.g., 'bed_occupancy', 'icu_usage', 'ppe_usage', 'ventilator_usage'
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)  # e.g., 'count', 'percentage'


class OWIDCovidMetric(Base):
    """Our World in Data COVID metrics"""
    __tablename__ = "owid_covid_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    new_cases = Column(Float, nullable=True)
    new_deaths = Column(Float, nullable=True)
    hosp_patients = Column(Float, nullable=True)
    icu_patients = Column(Float, nullable=True)
    tests_per_thousand = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

