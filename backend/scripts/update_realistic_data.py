"""
Update database with realistic outbreak data patterns
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.health_metrics import SearchTrend, PharmacyAggregate, HospitalUtilization
from app.models.risk_scores import RiskScore, Anomaly
from app.models.alerts import Alert
import random

# Realistic outbreak patterns by region
REGION_PATTERNS = {
    'US-CA': {
        'base_risk': 0.45,
        'trend': 'increasing',
        'primary_illness': 'Respiratory syncytial virus (RSV)',
        'hospital_pressure': 0.72
    },
    'US-NY': {
        'base_risk': 0.38,
        'trend': 'stable',
        'primary_illness': 'Seasonal influenza',
        'hospital_pressure': 0.65
    },
    'US-TX': {
        'base_risk': 0.52,
        'trend': 'increasing',
        'primary_illness': 'COVID-19 variant',
        'hospital_pressure': 0.68
    },
    'US-FL': {
        'base_risk': 0.41,
        'trend': 'decreasing',
        'primary_illness': 'Dengue fever',
        'hospital_pressure': 0.58
    },
    'US-IL': {
        'base_risk': 0.35,
        'trend': 'stable',
        'primary_illness': 'Influenza A',
        'hospital_pressure': 0.61
    }
}

def update_risk_scores():
    """Update risk scores with realistic patterns"""
    print("Updating risk scores with realistic outbreak patterns...")
    db: Session = SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        
        for region, pattern in REGION_PATTERNS.items():
            # Add some daily variation
            daily_variation = random.uniform(-0.05, 0.05)
            risk_prob = max(0.1, min(0.95, pattern['base_risk'] + daily_variation))
            
            if risk_prob < 0.3:
                risk_level = 'low'
            elif risk_prob < 0.5:
                risk_level = 'medium'
            elif risk_prob < 0.7:
                risk_level = 'high'
            else:
                risk_level = 'critical'
            
            factors = f"{pattern['primary_illness']} - {pattern['trend']} trend. "
            factors += f"Hospital utilization at {pattern['hospital_pressure']*100:.0f}%. "
            factors += "Multiple indicators suggest elevated risk."
            
            score = RiskScore(
                region_id=region,
                timestamp=now,
                risk_probability=risk_prob,
                risk_level=risk_level,
                contributing_factors=factors
            )
            db.add(score)
        
        db.commit()
        print(f"✓ Updated risk scores for {len(REGION_PATTERNS)} regions")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
    finally:
        db.close()

def update_search_trends():
    """Update search trends with realistic patterns"""
    print("Updating search trend data...")
    db: Session = SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        
        # Realistic keyword trends
        keyword_patterns = {
            'fever': (45, 85),
            'cough': (50, 90),
            'flu symptoms': (40, 75),
            'covid symptoms': (30, 60),
            'shortness of breath': (25, 50),
            'body aches': (35, 65)
        }
        
        for region in REGION_PATTERNS.keys():
            pattern = REGION_PATTERNS[region]
            intensity_multiplier = 0.8 if pattern['trend'] == 'decreasing' else 1.2 if pattern['trend'] == 'increasing' else 1.0
            
            for keyword, (min_val, max_val) in keyword_patterns.items():
                base_index = random.uniform(min_val, max_val)
                search_index = base_index * intensity_multiplier
                
                trend = SearchTrend(
                    region_id=region,
                    keyword=keyword,
                    search_index=search_index,
                    timestamp=now - timedelta(hours=random.randint(0, 6))
                )
                db.add(trend)
        
        db.commit()
        print(f"✓ Updated search trends for {len(REGION_PATTERNS)} regions")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
    finally:
        db.close()

def update_pharmacy_data():
    """Update pharmacy data with realistic patterns"""
    print("Updating pharmacy purchase data...")
    db: Session = SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        
        drug_categories = {
            'antipyretics': (800, 2500),
            'cough_suppressants': (600, 2000),
            'antivirals': (300, 1200),
            'decongestants': (500, 1800),
            'pain_relievers': (1000, 3000)
        }
        
        for region in REGION_PATTERNS.keys():
            pattern = REGION_PATTERNS[region]
            multiplier = 1.3 if pattern['trend'] == 'increasing' else 0.8 if pattern['trend'] == 'decreasing' else 1.0
            
            for category, (min_count, max_count) in drug_categories.items():
                count = int(random.uniform(min_count, max_count) * multiplier)
                
                pharmacy = PharmacyAggregate(
                    region_id=region,
                    drug_category=category,
                    count=count,
                    timestamp=now - timedelta(hours=random.randint(0, 12))
                )
                db.add(pharmacy)
        
        db.commit()
        print(f"✓ Updated pharmacy data for {len(REGION_PATTERNS)} regions")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
    finally:
        db.close()

def update_hospital_data():
    """Update hospital utilization with realistic patterns"""
    print("Updating hospital utilization metrics...")
    db: Session = SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        
        metric_types = ['bed_occupancy', 'icu_usage', 'er_visits', 'ppe_usage']
        
        for region in REGION_PATTERNS.keys():
            pattern = REGION_PATTERNS[region]
            base_pressure = pattern['hospital_pressure']
            
            for metric_type in metric_types:
                # ICU usage typically lower than bed occupancy
                if metric_type == 'icu_usage':
                    value = base_pressure * 0.7 + random.uniform(-0.05, 0.05)
                elif metric_type == 'er_visits':
                    value = base_pressure * 0.85 + random.uniform(-0.08, 0.08)
                else:
                    value = base_pressure + random.uniform(-0.05, 0.05)
                
                value = max(0.3, min(0.95, value))
                
                utilization = HospitalUtilization(
                    region_id=region,
                    metric_type=metric_type,
                    value=value,
                    unit='percentage',
                    timestamp=now - timedelta(hours=random.randint(0, 8))
                )
                db.add(utilization)
        
        db.commit()
        print(f"✓ Updated hospital metrics for {len(REGION_PATTERNS)} regions")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
    finally:
        db.close()

def create_alerts_for_high_risk():
    """Create alerts for high-risk regions"""
    print("Creating alerts for high-risk regions...")
    db: Session = SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        
        for region, pattern in REGION_PATTERNS.items():
            if pattern['base_risk'] > 0.5:  # High risk threshold
                # Check if alert already exists
                existing = db.query(Alert).filter(
                    Alert.region_id == region,
                    Alert.is_read == False
                ).first()
                
                if not existing:
                    alert = Alert(
                        region_id=region,
                        alert_type='risk_increase',
                        severity='high' if pattern['base_risk'] > 0.6 else 'medium',
                        title=f'Elevated Outbreak Risk in {region}',
                        message=f"{pattern['primary_illness']} showing {pattern['trend']} trend. Hospital capacity at {pattern['hospital_pressure']*100:.0f}%. Enhanced monitoring recommended.",
                        is_read=False,
                        is_acknowledged=False
                    )
                    db.add(alert)
        
        db.commit()
        print(f"✓ Created alerts for high-risk regions")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("HORIZON - Realistic Data Update Pipeline")
    print("="*70 + "\n")
    
    update_risk_scores()
    update_search_trends()
    update_pharmacy_data()
    update_hospital_data()
    create_alerts_for_high_risk()
    
    print("\n" + "="*70)
    print("✓ Data pipeline complete!")
    print("="*70 + "\n")
    print("Your Horizon platform now shows realistic outbreak patterns:")
    print("  • US-CA & US-TX: Increasing risk trends")
    print("  • US-NY & US-IL: Stable conditions")
    print("  • US-FL: Decreasing risk")
    print("\nRefresh your browser at http://localhost:3000 to see the updates!")

