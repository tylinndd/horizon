"""
Generate extensive realistic mock data for Horizon demo
Creates weeks of historical data with realistic patterns and trends
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.risk_scores import RiskScore, Anomaly
from app.models.alerts import Alert
from app.models.fintech import FundAllocation
from app.models.health_metrics import SearchTrend, PharmacyAggregate, HospitalUtilization
import random
import math

# All US states + DC
ALL_REGIONS = [
    "US-AL", "US-AK", "US-AZ", "US-AR", "US-CA", "US-CO", "US-CT", "US-DE",
    "US-FL", "US-GA", "US-HI", "US-ID", "US-IL", "US-IN", "US-IA", "US-KS",
    "US-KY", "US-LA", "US-ME", "US-MD", "US-MA", "US-MI", "US-MN", "US-MS",
    "US-MO", "US-MT", "US-NE", "US-NV", "US-NH", "US-NJ", "US-NM", "US-NY",
    "US-NC", "US-ND", "US-OH", "US-OK", "US-OR", "US-PA", "US-RI", "US-SC",
    "US-SD", "US-TN", "US-TX", "US-UT", "US-VT", "US-VA", "US-WA", "US-WV",
    "US-WI", "US-WY", "US-DC"
]

# Realistic region patterns - some regions have higher baseline risk
# Updated to include more high and critical risk regions for better visualization
REGION_BASELINES = {
    # Critical risk regions (0.75+)
    'US-CA': {'base_risk': 0.78, 'population_factor': 1.3, 'illness': 'RSV'},
    'US-TX': {'base_risk': 0.82, 'population_factor': 1.4, 'illness': 'COVID-19'},
    'US-FL': {'base_risk': 0.75, 'population_factor': 1.1, 'illness': 'Dengue'},
    
    # High risk regions (0.55-0.74)
    'US-NY': {'base_risk': 0.68, 'population_factor': 1.2, 'illness': 'Influenza'},
    'US-GA': {'base_risk': 0.64, 'population_factor': 1.2, 'illness': 'COVID-19'},
    'US-PA': {'base_risk': 0.62, 'population_factor': 1.1, 'illness': 'RSV'},
    'US-NC': {'base_risk': 0.59, 'population_factor': 1.1, 'illness': 'Influenza'},
    'US-AZ': {'base_risk': 0.66, 'population_factor': 1.2, 'illness': 'Respiratory illness'},
    'US-NV': {'base_risk': 0.61, 'population_factor': 1.1, 'illness': 'Influenza'},
    'US-TN': {'base_risk': 0.58, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-IN': {'base_risk': 0.63, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-MO': {'base_risk': 0.60, 'population_factor': 1.0, 'illness': 'COVID-19'},
    'US-MD': {'base_risk': 0.65, 'population_factor': 1.1, 'illness': 'RSV'},
    'US-WA': {'base_risk': 0.57, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-CO': {'base_risk': 0.64, 'population_factor': 1.1, 'illness': 'Respiratory illness'},
    
    # Medium risk regions (0.35-0.54)
    'US-IL': {'base_risk': 0.45, 'population_factor': 1.0, 'illness': 'Influenza A'},
    'US-OH': {'base_risk': 0.42, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-MI': {'base_risk': 0.48, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-VA': {'base_risk': 0.44, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-MA': {'base_risk': 0.46, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-NJ': {'base_risk': 0.43, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-WI': {'base_risk': 0.41, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-MN': {'base_risk': 0.39, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-SC': {'base_risk': 0.47, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-LA': {'base_risk': 0.45, 'population_factor': 1.0, 'illness': 'Respiratory illness'},
    'US-KY': {'base_risk': 0.40, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-OR': {'base_risk': 0.38, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-OK': {'base_risk': 0.44, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-CT': {'base_risk': 0.42, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-IA': {'base_risk': 0.39, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-UT': {'base_risk': 0.41, 'population_factor': 1.0, 'illness': 'Respiratory illness'},
    'US-AR': {'base_risk': 0.43, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-MS': {'base_risk': 0.46, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-KS': {'base_risk': 0.40, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-NM': {'base_risk': 0.38, 'population_factor': 1.0, 'illness': 'Respiratory illness'},
    'US-NE': {'base_risk': 0.37, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-WV': {'base_risk': 0.44, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-ID': {'base_risk': 0.36, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-HI': {'base_risk': 0.35, 'population_factor': 1.0, 'illness': 'Respiratory illness'},
    'US-NH': {'base_risk': 0.38, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-ME': {'base_risk': 0.36, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-RI': {'base_risk': 0.37, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-MT': {'base_risk': 0.35, 'population_factor': 1.0, 'illness': 'Respiratory illness'},
    'US-DE': {'base_risk': 0.38, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-SD': {'base_risk': 0.36, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-ND': {'base_risk': 0.35, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-AK': {'base_risk': 0.34, 'population_factor': 1.0, 'illness': 'Respiratory illness'},
    'US-VT': {'base_risk': 0.33, 'population_factor': 1.0, 'illness': 'Influenza'},
    'US-WY': {'base_risk': 0.32, 'population_factor': 1.0, 'illness': 'RSV'},
    'US-DC': {'base_risk': 0.45, 'population_factor': 1.0, 'illness': 'Influenza'},
}

# Symptom keywords for search trends
SYMPTOM_KEYWORDS = [
    'fever', 'cough', 'flu symptoms', 'covid symptoms', 'shortness of breath',
    'sore throat', 'body aches', 'loss of taste', 'headache', 'fatigue',
    'nausea', 'diarrhea', 'chills', 'congestion', 'runny nose'
]

# Drug categories
DRUG_CATEGORIES = [
    'antipyretics', 'cough_suppressants', 'antivirals', 'decongestants',
    'pain_relievers', 'antibiotics', 'antihistamines', 'bronchodilators'
]

# Hospital metric types
HOSPITAL_METRICS = [
    'bed_occupancy', 'icu_usage', 'er_visits', 'ppe_usage',
    'ventilator_usage', 'staff_shortage', 'medication_supply'
]


def get_region_baseline(region_id):
    """Get baseline risk for a region"""
    return REGION_BASELINES.get(region_id, {
        'base_risk': random.uniform(0.25, 0.45),
        'population_factor': random.uniform(0.8, 1.2),
        'illness': random.choice(['Influenza', 'RSV', 'COVID-19', 'Common Cold'])
    })


def generate_trend_value(base_value, days_ago, trend_type='stable', noise=0.05):
    """Generate a value with realistic trend over time"""
    # Add trend component
    if trend_type == 'increasing':
        trend = 0.02 * (30 - days_ago) / 30  # Gradually increase
    elif trend_type == 'decreasing':
        trend = -0.02 * (30 - days_ago) / 30  # Gradually decrease
    elif trend_type == 'spike':
        # Spike around day 15
        spike = 0.3 * math.exp(-((days_ago - 15) ** 2) / 50)
        trend = spike
    else:  # stable
        trend = 0
    
    # Add weekly cycle (lower on weekends)
    day_of_week = (datetime.now(timezone.utc) - timedelta(days=days_ago)).weekday()
    weekly_cycle = -0.05 if day_of_week >= 5 else 0  # Weekend effect
    
    # Add noise
    noise_component = random.uniform(-noise, noise)
    
    value = base_value + trend + weekly_cycle + noise_component
    return max(0.1, min(0.95, value))


def generate_risk_scores(db: Session, days_back=30):
    """Generate historical risk scores"""
    print(f"Generating risk scores for {len(ALL_REGIONS)} regions over {days_back} days...")
    
    now = datetime.now(timezone.utc)
    count = 0
    
    for region in ALL_REGIONS:
        baseline = get_region_baseline(region)
        base_risk = baseline['base_risk']
        
        # Determine trend type
        if base_risk > 0.5:
            trend_type = random.choice(['increasing', 'spike'])
        elif base_risk < 0.3:
            trend_type = 'decreasing'
        else:
            trend_type = random.choice(['stable', 'increasing'])
        
        # Generate daily scores
        for day in range(days_back):
            timestamp = now - timedelta(days=day, hours=random.randint(0, 23))
            # Use less noise for the latest day (day 0) to preserve intended risk levels
            noise_level = 0.03 if day == 0 else 0.08
            risk_prob = generate_trend_value(base_risk, day, trend_type, noise=noise_level)
            
            # Ensure risk levels match the intended baselines for latest scores
            if day == 0:
                # For latest scores, preserve the intended risk level
                if base_risk >= 0.75:
                    risk_prob = max(0.75, min(0.95, risk_prob))
                elif base_risk >= 0.55:
                    risk_prob = max(0.55, min(0.74, risk_prob))
                elif base_risk >= 0.35:
                    risk_prob = max(0.35, min(0.54, risk_prob))
                else:
                    risk_prob = max(0.1, min(0.34, risk_prob))
            
            if risk_prob < 0.25:
                risk_level = 'low'
            elif risk_prob < 0.5:
                risk_level = 'medium'
            elif risk_prob < 0.75:
                risk_level = 'high'
            else:
                risk_level = 'critical'
            
            factors = f"{baseline['illness']} activity. "
            factors += f"Population density factor: {baseline['population_factor']:.2f}. "
            factors += f"Trend: {trend_type}. "
            factors += f"Multiple health indicators showing elevated signals."
            
            score = RiskScore(
                region_id=region,
                timestamp=timestamp,
                risk_probability=risk_prob,
                risk_level=risk_level,
                contributing_factors=factors,
                model_version='v1.2'
            )
            db.add(score)
            count += 1
            
            # Commit every 100 records
            if count % 100 == 0:
                db.commit()
    
    db.commit()
    print(f"✓ Generated {count} risk score records")


def generate_search_trends(db: Session, days_back=30):
    """Generate historical search trend data"""
    print(f"Generating search trends for {len(ALL_REGIONS)} regions over {days_back} days...")
    
    now = datetime.now(timezone.utc)
    count = 0
    
    keyword_baselines = {
        'fever': (40, 80),
        'cough': (45, 85),
        'flu symptoms': (35, 70),
        'covid symptoms': (25, 55),
        'shortness of breath': (20, 45),
        'sore throat': (30, 60),
        'body aches': (25, 50),
        'loss of taste': (15, 35),
        'headache': (35, 65),
        'fatigue': (30, 55),
        'nausea': (20, 40),
        'diarrhea': (15, 30),
        'chills': (25, 50),
        'congestion': (40, 70),
        'runny nose': (35, 65)
    }
    
    for region in ALL_REGIONS:
        baseline = get_region_baseline(region)
        multiplier = baseline['population_factor']
        
        # Generate data every 6 hours
        for day in range(days_back):
            for hour_offset in [0, 6, 12, 18]:
                timestamp = now - timedelta(days=day, hours=hour_offset + random.randint(0, 5))
                
                for keyword in SYMPTOM_KEYWORDS:
                    min_val, max_val = keyword_baselines.get(keyword, (20, 60))
                    base_index = random.uniform(min_val, max_val) * multiplier
                    
                    # Add correlation with risk level
                    risk_multiplier = 1.0 + (baseline['base_risk'] - 0.35) * 0.5
                    search_index = base_index * risk_multiplier
                    search_index = max(0, min(100, search_index))
                    
                    trend = SearchTrend(
                        region_id=region,
                        keyword=keyword,
                        search_index=search_index,
                        timestamp=timestamp
                    )
                    db.add(trend)
                    count += 1
                    
                    if count % 500 == 0:
                        db.commit()
    
    db.commit()
    print(f"✓ Generated {count} search trend records")


def generate_pharmacy_data(db: Session, days_back=30):
    """Generate historical pharmacy purchase data"""
    print(f"Generating pharmacy data for {len(ALL_REGIONS)} regions over {days_back} days...")
    
    now = datetime.now(timezone.utc)
    count = 0
    
    drug_baselines = {
        'antipyretics': (800, 2500),
        'cough_suppressants': (600, 2000),
        'antivirals': (300, 1200),
        'decongestants': (500, 1800),
        'pain_relievers': (1000, 3000),
        'antibiotics': (400, 1500),
        'antihistamines': (700, 2200),
        'bronchodilators': (200, 800)
    }
    
    for region in ALL_REGIONS:
        baseline = get_region_baseline(region)
        multiplier = baseline['population_factor']
        
        # Generate daily data
        for day in range(days_back):
            timestamp = now - timedelta(days=day, hours=random.randint(0, 23))
            
            for category in DRUG_CATEGORIES:
                min_count, max_count = drug_baselines.get(category, (500, 2000))
                base_count = random.uniform(min_count, max_count) * multiplier
                
                # Correlate with risk level
                risk_multiplier = 1.0 + (baseline['base_risk'] - 0.35) * 0.6
                count_value = int(base_count * risk_multiplier)
                
                pharmacy = PharmacyAggregate(
                    region_id=region,
                    drug_category=category,
                    count=count_value,
                    timestamp=timestamp
                )
                db.add(pharmacy)
                count += 1
                
                if count % 500 == 0:
                    db.commit()
    
    db.commit()
    print(f"✓ Generated {count} pharmacy records")


def generate_hospital_data(db: Session, days_back=30):
    """Generate historical hospital utilization data"""
    print(f"Generating hospital data for {len(ALL_REGIONS)} regions over {days_back} days...")
    
    now = datetime.now(timezone.utc)
    count = 0
    
    for region in ALL_REGIONS:
        baseline = get_region_baseline(region)
        base_pressure = baseline['base_risk'] * 1.2  # Convert risk to hospital pressure
        base_pressure = min(0.85, base_pressure)
        
        # Generate data every 12 hours
        for day in range(days_back):
            for hour_offset in [0, 12]:
                timestamp = now - timedelta(days=day, hours=hour_offset + random.randint(0, 11))
                
                for metric_type in HOSPITAL_METRICS:
                    # Different metrics have different baselines
                    if metric_type == 'icu_usage':
                        value = base_pressure * 0.6 + random.uniform(-0.1, 0.1)
                    elif metric_type == 'er_visits':
                        value = base_pressure * 0.9 + random.uniform(-0.15, 0.15)
                    elif metric_type == 'ventilator_usage':
                        value = base_pressure * 0.4 + random.uniform(-0.08, 0.08)
                    elif metric_type == 'staff_shortage':
                        value = base_pressure * 0.5 + random.uniform(-0.1, 0.1)
                    elif metric_type == 'medication_supply':
                        value = 1.0 - (base_pressure * 0.3) + random.uniform(-0.1, 0.1)  # Inverse
                    else:
                        value = base_pressure + random.uniform(-0.1, 0.1)
                    
                    value = max(0.2, min(0.95, value))
                    
                    utilization = HospitalUtilization(
                        region_id=region,
                        metric_type=metric_type,
                        value=value,
                        unit='percentage' if 'usage' in metric_type or 'occupancy' in metric_type else 'count',
                        timestamp=timestamp
                    )
                    db.add(utilization)
                    count += 1
                    
                    if count % 500 == 0:
                        db.commit()
    
    db.commit()
    print(f"✓ Generated {count} hospital utilization records")


def generate_anomalies(db: Session):
    """Generate detected anomalies"""
    print("Generating anomaly records...")
    
    now = datetime.now(timezone.utc)
    count = 0
    
    # Generate anomalies for high-risk regions
    high_risk_regions = [r for r in ALL_REGIONS if get_region_baseline(r)['base_risk'] > 0.45]
    
    anomaly_types = [
        ('pharmacy', 'Spike in antipyretic purchases', 0.85),
        ('search_trend', 'Unusual increase in symptom searches', 0.75),
        ('hospital_utilization', 'ICU capacity exceeded threshold', 0.90),
        ('pharmacy', 'Antiviral demand surge', 0.80),
        ('search_trend', 'Fever searches 3x baseline', 0.70)
    ]
    
    for region in high_risk_regions[:10]:  # Top 10 high-risk regions
        for metric_type, description, anomaly_score in anomaly_types:
            timestamp = now - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
            
            anomaly = Anomaly(
                region_id=region,
                timestamp=timestamp,
                metric_type=metric_type,
                metric_value=random.uniform(0.7, 0.95),
                anomaly_score=anomaly_score,
                is_anomaly=True,
                description=description
            )
            db.add(anomaly)
            count += 1
    
    db.commit()
    print(f"✓ Generated {count} anomaly records")


def generate_alerts(db: Session):
    """Generate alerts for high-risk situations"""
    print("Generating alerts...")
    
    now = datetime.now(timezone.utc)
    count = 0
    
    alert_templates = [
        {
            'type': 'risk_increase',
            'severity': 'critical',
            'title_template': 'Critical Outbreak Risk in {region}',
            'message_template': 'Multiple indicators show critical outbreak risk. Hospital capacity at {capacity}%. Immediate action recommended.'
        },
        {
            'type': 'anomaly_detected',
            'severity': 'high',
            'title_template': 'Anomaly Detected in {region}',
            'message_template': 'Unusual pattern detected in health indicators. Review metrics and consider enhanced monitoring.'
        },
        {
            'type': 'hospital_capacity',
            'severity': 'high',
            'title_template': 'Hospital Capacity Alert for {region}',
            'message_template': 'Hospital utilization approaching capacity limits. ICU usage at {capacity}%.'
        },
        {
            'type': 'pharmacy_surge',
            'severity': 'medium',
            'title_template': 'Medication Purchase Surge in {region}',
            'message_template': 'Significant increase in symptom-related medication purchases detected.'
        }
    ]
    
    # Generate alerts for high-risk regions
    high_risk_regions = sorted(
        [(r, get_region_baseline(r)['base_risk']) for r in ALL_REGIONS],
        key=lambda x: x[1],
        reverse=True
    )[:15]  # Top 15 regions
    
    for region, risk_prob in high_risk_regions:
        baseline = get_region_baseline(region)
        
        # Create 1-3 alerts per high-risk region
        num_alerts = random.randint(1, 3)
        for _ in range(num_alerts):
            template = random.choice(alert_templates)
            
            # Adjust severity based on risk
            if risk_prob > 0.7:
                severity = 'critical'
            elif risk_prob > 0.55:
                severity = 'high'
            else:
                severity = 'medium'
            
            capacity = int(baseline['base_risk'] * 120)
            capacity = min(95, capacity)
            
            alert = Alert(
                region_id=region,
                alert_type=template['type'],
                severity=severity,
                title=template['title_template'].format(region=region),
                message=template['message_template'].format(
                    region=region,
                    capacity=capacity,
                    illness=baseline['illness']
                ),
                is_read=random.choice([True, False]) if risk_prob < 0.6 else False,
                is_acknowledged=False
            )
            db.add(alert)
            count += 1
    
    db.commit()
    print(f"✓ Generated {count} alert records")


def generate_fund_allocations(db: Session):
    """Generate fund allocation records"""
    print("Generating fund allocations...")
    
    now = datetime.now(timezone.utc)
    count = 0
    
    # Generate allocations for high-risk regions
    high_risk_regions = sorted(
        [(r, get_region_baseline(r)['base_risk']) for r in ALL_REGIONS],
        key=lambda x: x[1],
        reverse=True
    )[:20]  # Top 20 regions
    
    for region, risk_prob in high_risk_regions:
        # Generate 1-2 allocations per region
        for _ in range(random.randint(1, 2)):
            timestamp = now - timedelta(days=random.randint(0, 14))
            
            # Allocation amount correlates with risk
            base_amount = 100000
            risk_multiplier = 1.0 + (risk_prob - 0.35) * 2.0
            allocated_amount = base_amount * risk_multiplier * random.uniform(0.8, 1.5)
            
            allocation = FundAllocation(
                region_id=region,
                timestamp=timestamp,
                allocated_amount=allocated_amount,
                currency='USD',
                allocation_reason=f'Emergency response allocation for {region} based on elevated outbreak risk indicators',
                status='simulated'
            )
            db.add(allocation)
            count += 1
    
    db.commit()
    print(f"✓ Generated {count} fund allocation records")


def main():
    """Main function to generate all mock data"""
    print("\n" + "="*70)
    print("HORIZON - Extensive Mock Data Generation")
    print("="*70 + "\n")
    print("This will generate realistic mock data for:")
    print(f"  • {len(ALL_REGIONS)} regions")
    print("  • 30 days of historical data")
    print("  • Multiple data types (risk scores, trends, pharmacy, hospital)")
    print("\nThis may take a few minutes...\n")
    
    db: Session = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing mock data...")
        db.query(RiskScore).delete()
        db.query(SearchTrend).delete()
        db.query(PharmacyAggregate).delete()
        db.query(HospitalUtilization).delete()
        db.query(Anomaly).delete()
        db.query(Alert).delete()
        db.query(FundAllocation).delete()
        db.commit()
        print("✓ Cleared existing data\n")
        
        # Generate all data types
        generate_risk_scores(db, days_back=30)
        generate_search_trends(db, days_back=30)
        generate_pharmacy_data(db, days_back=30)
        generate_hospital_data(db, days_back=30)
        generate_anomalies(db)
        generate_alerts(db)
        generate_fund_allocations(db)
        
        print("\n" + "="*70)
        print("✓ Extensive mock data generation complete!")
        print("="*70 + "\n")
        print("Your Horizon platform now has:")
        print(f"  • Risk scores for {len(ALL_REGIONS)} regions over 30 days")
        print("  • Search trends with realistic patterns")
        print("  • Pharmacy purchase data")
        print("  • Hospital utilization metrics")
        print("  • Detected anomalies")
        print("  • Active alerts")
        print("  • Fund allocations")
        print("\nRefresh your browser at http://localhost:3000 to see the data!")
        print("\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error generating data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

