"""
Seed database with sample data for testing
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.risk_scores import RiskScore, Anomaly
from app.models.alerts import Alert
from app.models.fintech import FundAllocation
from app.models.health_metrics import SearchTrend, PharmacyAggregate, HospitalUtilization
import random

def seed_sample_data():
    """Seed database with sample data"""
    db: Session = SessionLocal()
    
    try:
        regions = ['US-CA', 'US-NY', 'US-TX', 'US-FL', 'US-IL']
        now = datetime.now(timezone.utc)
        
        # Create risk scores
        print("Creating risk scores...")
        for region in regions:
            risk_prob = random.uniform(0.1, 0.9)
            risk_level = 'low' if risk_prob < 0.25 else 'medium' if risk_prob < 0.5 else 'high' if risk_prob < 0.75 else 'critical'
            
            score = RiskScore(
                region_id=region,
                timestamp=now,
                risk_probability=risk_prob,
                risk_level=risk_level,
                contributing_factors=f"Sample factors for {region}"
            )
            db.add(score)
        
        # Create search trends
        print("Creating search trends...")
        keywords = ['fever', 'cough', 'flu symptoms']
        for region in regions:
            for keyword in keywords:
                trend = SearchTrend(
                    region_id=region,
                    keyword=keyword,
                    search_index=random.uniform(0, 100),
                    timestamp=now - timedelta(hours=random.randint(0, 24))
                )
                db.add(trend)
        
        # Create pharmacy aggregates
        print("Creating pharmacy data...")
        drug_categories = ['antipyretics', 'cough_suppressants', 'antivirals']
        for region in regions:
            for category in drug_categories:
                pharmacy = PharmacyAggregate(
                    region_id=region,
                    drug_category=category,
                    count=random.randint(100, 1000),
                    timestamp=now - timedelta(hours=random.randint(0, 24))
                )
                db.add(pharmacy)
        
        # Create hospital utilization
        print("Creating hospital utilization data...")
        metric_types = ['bed_occupancy', 'icu_usage', 'ppe_usage']
        for region in regions:
            for metric_type in metric_types:
                utilization = HospitalUtilization(
                    region_id=region,
                    metric_type=metric_type,
                    value=random.uniform(0.3, 0.95),
                    unit='percentage',
                    timestamp=now - timedelta(hours=random.randint(0, 24))
                )
                db.add(utilization)
        
        # Create alerts for high-risk regions
        print("Creating alerts...")
        high_risk_regions = ['US-CA', 'US-NY']
        for region in high_risk_regions:
            alert = Alert(
                region_id=region,
                alert_type='risk_increase',
                severity='high',
                title=f'High Risk Detected in {region}',
                message=f'Outbreak risk has increased significantly in {region}. Review metrics and consider preventive measures.',
                is_read=False,
                is_acknowledged=False
            )
            db.add(alert)
        
        # Create fund allocations
        print("Creating fund allocations...")
        for region in high_risk_regions:
            allocation = FundAllocation(
                region_id=region,
                timestamp=now,
                allocated_amount=random.uniform(100000, 500000),
                currency='USD',
                allocation_reason=f'Emergency response allocation for {region}',
                status='simulated'
            )
            db.add(allocation)
        
        db.commit()
        print("Sample data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_sample_data()

