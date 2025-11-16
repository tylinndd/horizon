"""
Generate mock data for Emory Hospital integration
Creates realistic budget, resource allocation, and recommendation data
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.hospital_insights import HospitalBudget, ResourceAllocation, HospitalRecommendation
from app.models.risk_scores import RiskScore
import random
import math

# Emory Hospital constants
EMORY_TENANT_ID = 1  # Emory Hospital tenant ID
EMORY_FACILITY_ID = "emory-main"
EMORY_FACILITY_NAME = "Emory University Hospital"
EMORY_REGION_ID = "US-GA"  # Georgia

# Base budget for Emory Hospital (annual budget in millions)
EMORY_ANNUAL_BUDGET = 2500.0  # $2.5 billion annual budget


def get_current_risk_score(db: Session):
    """Get the current risk score for Georgia"""
    risk_score = db.query(RiskScore).filter(
        RiskScore.region_id == EMORY_REGION_ID
    ).order_by(RiskScore.timestamp.desc()).first()
    
    if risk_score:
        return risk_score.risk_probability, risk_score.risk_level
    return 0.64, "high"  # Default for Georgia based on mock data


def generate_budget_data(db: Session):
    """Generate budget data for Emory Hospital"""
    print("Generating Emory Hospital budget data...")
    
    now = datetime.now(timezone.utc)
    risk_prob, risk_level = get_current_risk_score(db)
    
    # Generate quarterly budgets for the past year
    quarters = []
    for quarter in range(4):
        quarter_start = now - timedelta(days=90 * (3 - quarter))
        quarter_end = quarter_start + timedelta(days=90)
        quarters.append((quarter_start, quarter_end))
    
    # Also create current quarter
    current_quarter_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_quarter_end = current_quarter_start + timedelta(days=90)
    quarters.append((current_quarter_start, current_quarter_end))
    
    for quarter_start, quarter_end in quarters:
        # Quarterly budget is 1/4 of annual
        quarterly_budget = EMORY_ANNUAL_BUDGET / 4
        
        # Adjust for risk - higher risk means more budget needed
        risk_multiplier = 1.0 + (risk_prob - 0.5) * 0.2
        risk_adjusted_budget = quarterly_budget * risk_multiplier
        
        # Allocate budget across categories
        # Emergency preparedness gets more during high risk
        emergency_pct = 0.15 + (risk_prob - 0.5) * 0.1
        staff_pct = 0.35
        equipment_pct = 0.20
        infrastructure_pct = 0.15
        research_pct = 0.10
        other_pct = 0.05
        
        emergency_preparedness = quarterly_budget * emergency_pct
        staff_resources = quarterly_budget * staff_pct
        equipment_supplies = quarterly_budget * equipment_pct
        infrastructure = quarterly_budget * infrastructure_pct
        research_development = quarterly_budget * research_pct
        other = quarterly_budget * other_pct
        
        allocated_budget = emergency_preparedness + staff_resources + equipment_supplies + infrastructure + research_development + other
        available_budget = quarterly_budget - allocated_budget
        
        # Recommended allocation adjustments based on risk
        recommended_allocation = {
            "emergency_preparedness": {
                "current": emergency_preparedness,
                "recommended": emergency_preparedness * (1.0 + (risk_prob - 0.5) * 0.3),
                "reason": f"Increase emergency preparedness funding due to {risk_level} risk level"
            },
            "staff_resources": {
                "current": staff_resources,
                "recommended": staff_resources * (1.0 + (risk_prob - 0.5) * 0.15),
                "reason": "Maintain adequate staffing levels for potential surge"
            },
            "equipment_supplies": {
                "current": equipment_supplies,
                "recommended": equipment_supplies * (1.0 + (risk_prob - 0.5) * 0.25),
                "reason": "Ensure adequate PPE and medical equipment inventory"
            }
        }
        
        budget = HospitalBudget(
            tenant_id=EMORY_TENANT_ID,
            facility_id=EMORY_FACILITY_ID,
            facility_name=EMORY_FACILITY_NAME,
            timestamp=quarter_start,
            total_budget=quarterly_budget,
            allocated_budget=allocated_budget,
            available_budget=available_budget,
            emergency_preparedness=emergency_preparedness,
            staff_resources=staff_resources,
            equipment_supplies=equipment_supplies,
            infrastructure=infrastructure,
            research_development=research_development,
            other=other,
            recommended_allocation=recommended_allocation,
            risk_adjusted_budget=risk_adjusted_budget,
            currency="USD",
            period_start=quarter_start,
            period_end=quarter_end
        )
        db.add(budget)
    
    db.commit()
    print(f"✓ Generated {len(quarters)} budget records")


def generate_resource_allocations(db: Session):
    """Generate resource allocation recommendations"""
    print("Generating resource allocation recommendations...")
    
    now = datetime.now(timezone.utc)
    risk_prob, risk_level = get_current_risk_score(db)
    
    # Resource types with realistic data
    resources = [
        {
            "type": "staff",
            "current_capacity": 3500,  # Number of staff
            "base_utilization": 0.75,
            "priority": "critical" if risk_prob > 0.6 else "high",
            "reason": "Maintain adequate clinical and support staff for patient care surge capacity"
        },
        {
            "type": "equipment",
            "current_capacity": 150,  # Ventilators, ICU beds, etc.
            "base_utilization": 0.68,
            "priority": "high" if risk_prob > 0.55 else "medium",
            "reason": "Ensure critical care equipment availability for respiratory illness cases"
        },
        {
            "type": "supplies",
            "current_capacity": 45,  # Days of supply
            "base_utilization": 0.72,
            "priority": "high" if risk_prob > 0.6 else "medium",
            "reason": "Maintain adequate PPE and medical supply inventory for outbreak response"
        },
        {
            "type": "beds",
            "current_capacity": 733,  # Total beds
            "base_utilization": 0.78,
            "priority": "critical" if risk_prob > 0.65 else "high",
            "reason": "Optimize bed capacity and prepare for potential patient surge"
        },
        {
            "type": "medication",
            "current_capacity": 30,  # Days of critical medications
            "base_utilization": 0.70,
            "priority": "high" if risk_prob > 0.55 else "medium",
            "reason": "Ensure adequate antiviral and critical medication stockpiles"
        }
    ]
    
    for resource in resources:
        utilization_rate = resource["base_utilization"] + (risk_prob - 0.5) * 0.15
        utilization_rate = max(0.5, min(0.95, utilization_rate))
        
        # Recommended capacity increase based on risk
        capacity_multiplier = 1.0 + (risk_prob - 0.5) * 0.3
        recommended_capacity = resource["current_capacity"] * capacity_multiplier
        
        # Allocation increase recommendation
        allocation_increase = (recommended_capacity - resource["current_capacity"]) / resource["current_capacity"]
        recommended_allocation = resource["current_capacity"] * (1.0 + allocation_increase)
        
        allocation = ResourceAllocation(
            tenant_id=EMORY_TENANT_ID,
            facility_id=EMORY_FACILITY_ID,
            facility_name=EMORY_FACILITY_NAME,
            timestamp=now - timedelta(days=random.randint(0, 7)),
            resource_type=resource["type"],
            current_capacity=resource["current_capacity"],
            recommended_capacity=recommended_capacity,
            utilization_rate=utilization_rate,
            current_allocation=resource["current_capacity"],
            recommended_allocation=recommended_allocation,
            allocation_reason=resource["reason"],
            priority_level=resource["priority"],
            risk_level=risk_level,
            status="recommended"
        )
        db.add(allocation)
    
    db.commit()
    print(f"✓ Generated {len(resources)} resource allocation records")


def generate_recommendations(db: Session):
    """Generate AI-powered recommendations for Emory Hospital"""
    print("Generating hospital recommendations...")
    
    now = datetime.now(timezone.utc)
    risk_prob, risk_level = get_current_risk_score(db)
    
    recommendations = [
        {
            "type": "budget",
            "title": "Increase Emergency Preparedness Budget Allocation",
            "description": f"Based on current {risk_level} risk level in Georgia, recommend increasing emergency preparedness budget by 15-20% to ensure adequate surge capacity and response capabilities.",
            "priority": "critical" if risk_prob > 0.65 else "high",
            "impact": "Improve outbreak response readiness by 25%",
            "cost": 45.0,  # Millions
            "savings": None,
            "steps": [
                "Review current emergency preparedness protocols",
                "Allocate additional $45M to emergency preparedness fund",
                "Increase PPE inventory by 30%",
                "Enhance surge capacity planning",
                "Conduct emergency response drills"
            ],
            "timeframe": "2-3 weeks"
        },
        {
            "type": "resource",
            "title": "Optimize Staffing Levels for Potential Surge",
            "description": "Current utilization at 78% suggests limited surge capacity. Recommend hiring 150 additional clinical staff and establishing on-call pool of 200 healthcare workers.",
            "priority": "high",
            "impact": "Increase surge capacity by 30%",
            "cost": 12.5,  # Millions annually
            "savings": None,
            "steps": [
                "Identify critical staffing gaps",
                "Launch recruitment campaign for clinical staff",
                "Establish on-call healthcare worker pool",
                "Implement flexible scheduling system",
                "Provide surge capacity training"
            ],
            "timeframe": "1-2 months"
        },
        {
            "type": "operational",
            "title": "Implement Predictive Analytics for Resource Planning",
            "description": "Deploy AI-powered predictive models to forecast patient volumes and optimize resource allocation based on real-time health indicators.",
            "priority": "medium",
            "impact": "Reduce operational costs by 8-12% through better resource utilization",
            "cost": 2.5,
            "savings": 15.0,  # Annual savings
            "steps": [
                "Integrate Horizon platform data feeds",
                "Deploy predictive analytics dashboard",
                "Train staff on new tools",
                "Establish automated alerting system",
                "Monitor and optimize predictions"
            ],
            "timeframe": "3-4 weeks"
        },
        {
            "type": "preparedness",
            "title": "Enhance ICU Capacity and Ventilator Inventory",
            "description": f"With {risk_level} risk level indicating potential respiratory illness surge, recommend increasing ICU bed capacity by 20% and ventilator inventory by 25%.",
            "priority": "critical" if risk_prob > 0.65 else "high",
            "impact": "Increase critical care capacity by 20%",
            "cost": 8.5,
            "savings": None,
            "steps": [
                "Assess current ICU capacity",
                "Procure additional ventilators",
                "Plan ICU expansion or conversion",
                "Train staff on new equipment",
                "Establish maintenance protocols"
            ],
            "timeframe": "4-6 weeks"
        },
        {
            "type": "budget",
            "title": "Optimize Supply Chain and Inventory Management",
            "description": "Implement just-in-time inventory system with automated reordering to reduce costs while maintaining adequate stock levels for outbreak response.",
            "priority": "medium",
            "impact": "Reduce inventory costs by 15% while improving availability",
            "cost": 1.2,
            "savings": 3.5,  # Annual savings
            "steps": [
                "Audit current inventory management",
                "Implement automated inventory system",
                "Establish supplier partnerships",
                "Set up automated reordering",
                "Monitor and optimize stock levels"
            ],
            "timeframe": "2-3 months"
        },
        {
            "type": "operational",
            "title": "Establish Telemedicine Infrastructure for Outbreak Response",
            "description": "Expand telemedicine capabilities to handle increased patient volume during outbreaks while reducing exposure risk.",
            "priority": "high" if risk_prob > 0.6 else "medium",
            "impact": "Increase patient capacity by 40% without physical expansion",
            "cost": 3.8,
            "savings": 5.2,  # Annual savings from reduced overhead
            "steps": [
                "Upgrade telemedicine platform",
                "Train clinical staff on telemedicine",
                "Establish telemedicine protocols",
                "Integrate with EMR system",
                "Launch patient education campaign"
            ],
            "timeframe": "3-5 weeks"
        }
    ]
    
    # Adjust recommendations based on risk level
    for rec in recommendations:
        if risk_prob > 0.7:
            rec["priority"] = "critical" if rec["priority"] == "high" else rec["priority"]
        
        recommendation = HospitalRecommendation(
            tenant_id=EMORY_TENANT_ID,
            facility_id=EMORY_FACILITY_ID,
            facility_name=EMORY_FACILITY_NAME,
            timestamp=now - timedelta(days=random.randint(0, 14)),
            recommendation_type=rec["type"],
            title=rec["title"],
            description=rec["description"],
            priority=rec["priority"],
            estimated_impact=rec["impact"],
            estimated_cost=rec["cost"],
            estimated_savings=rec.get("savings"),
            implementation_steps=rec["steps"],
            timeframe=rec["timeframe"],
            status="pending" if random.random() > 0.3 else "in_progress"
        )
        db.add(recommendation)
    
    db.commit()
    print(f"✓ Generated {len(recommendations)} recommendation records")


def main():
    """Main function to generate Emory Hospital mock data"""
    print("\n" + "="*70)
    print("EMORY HOSPITAL - Mock Data Generation")
    print("="*70 + "\n")
    print("Generating realistic mock data for:")
    print(f"  • Facility: {EMORY_FACILITY_NAME}")
    print(f"  • Facility ID: {EMORY_FACILITY_ID}")
    print(f"  • Region: {EMORY_REGION_ID}")
    print(f"  • Tenant ID: {EMORY_TENANT_ID}")
    print("\n")
    
    db: Session = SessionLocal()
    
    try:
        # Clear existing Emory data (optional)
        print("Clearing existing Emory Hospital data...")
        db.query(HospitalBudget).filter(HospitalBudget.tenant_id == EMORY_TENANT_ID).delete()
        db.query(ResourceAllocation).filter(ResourceAllocation.tenant_id == EMORY_TENANT_ID).delete()
        db.query(HospitalRecommendation).filter(HospitalRecommendation.tenant_id == EMORY_TENANT_ID).delete()
        db.commit()
        print("✓ Cleared existing data\n")
        
        # Generate all data types
        generate_budget_data(db)
        generate_resource_allocations(db)
        generate_recommendations(db)
        
        print("\n" + "="*70)
        print("✓ Emory Hospital mock data generation complete!")
        print("="*70 + "\n")
        print("Generated data includes:")
        print("  • Budget allocations and recommendations")
        print("  • Resource allocation recommendations")
        print("  • AI-powered operational recommendations")
        print("\nAccess Emory Hospital dashboard at:")
        print("  http://localhost:3000/hospital/emory")
        print("\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error generating data: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

