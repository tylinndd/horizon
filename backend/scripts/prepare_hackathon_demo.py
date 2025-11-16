"""
Prepare Horizon for hackathon demo - intelligently loads data
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import argparse
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.risk_scores import RiskScore
from app.models.health_metrics import SearchTrend, PharmacyAggregate, HospitalUtilization, OWIDCovidMetric


def check_data_exists():
    """Check if database has sufficient data for demo"""
    db: Session = SessionLocal()
    try:
        risk_count = db.query(RiskScore).count()
        search_count = db.query(SearchTrend).count()
        pharmacy_count = db.query(PharmacyAggregate).count()
        hospital_count = db.query(HospitalUtilization).count()
        owid_count = db.query(OWIDCovidMetric).count()
        
        print(f"\nCurrent database status:")
        print(f"  Risk Scores: {risk_count}")
        print(f"  Search Trends: {search_count}")
        print(f"  Pharmacy Data: {pharmacy_count}")
        print(f"  Hospital Utilization: {hospital_count}")
        print(f"  OWID Metrics: {owid_count}")
        
        # Consider sufficient if we have at least some risk scores
        return risk_count > 0
    finally:
        db.close()


def load_real_data():
    """Try to load real data from APIs"""
    print("\n" + "="*60)
    print("Attempting to load REAL data from APIs...")
    print("="*60 + "\n")
    
    try:
        # Import and run fetch_real_data
        from scripts.fetch_real_data import (
            fetch_owid_data,
            load_owid_to_db,
            generate_risk_scores_from_real_data,
            update_search_trends
        )
        
        # Fetch OWID data
        owid_df = fetch_owid_data()
        if owid_df is not None:
            load_owid_to_db(owid_df)
            generate_risk_scores_from_real_data()
        else:
            print("⚠️  OWID data fetch failed, continuing with other sources...")
        
        # Try Google Trends (may fail due to rate limits)
        try:
            update_search_trends()
        except Exception as e:
            print(f"⚠️  Google Trends update failed: {e}")
            print("   This is common - continuing with other data sources...")
        
        print("\n✓ Real data loading complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error loading real data: {e}")
        return False


def load_mock_data():
    """Load mock/sample data"""
    print("\n" + "="*60)
    print("Loading MOCK/SAMPLE data...")
    print("="*60 + "\n")
    
    try:
        from scripts.seed_data import seed_sample_data
        seed_sample_data()
        print("\n✓ Mock data loaded successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Error loading mock data: {e}")
        return False


def load_local_datasets():
    """Load local CSV datasets if available"""
    print("\n" + "="*60)
    print("Attempting to load LOCAL CSV datasets...")
    print("="*60 + "\n")
    
    try:
        from scripts.ingest_local_datasets import main as ingest_local
        ingest_local()
        print("\n✓ Local datasets loaded!")
        return True
    except Exception as e:
        print(f"\n⚠️  Local dataset ingestion skipped: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Prepare Horizon database for hackathon demo"
    )
    parser.add_argument(
        "--mode",
        choices=["real", "mock", "hybrid", "check"],
        default="hybrid",
        help="Data loading mode: real (APIs only), mock (sample data), hybrid (try real, fallback to mock), check (just check status)"
    )
    parser.add_argument(
        "--include-local",
        action="store_true",
        help="Also load local CSV datasets"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("HORIZON - Hackathon Demo Preparation")
    print("="*60)
    
    if args.mode == "check":
        has_data = check_data_exists()
        if has_data:
            print("\n✓ Database has data - ready for demo!")
        else:
            print("\n⚠️  Database is empty - run with --mode hybrid to load data")
        return
    
    # Check current status
    has_data = check_data_exists()
    
    if args.mode == "real":
        success = load_real_data()
        if not success:
            print("\n⚠️  Real data loading failed. Consider using --mode hybrid")
    
    elif args.mode == "mock":
        load_mock_data()
    
    elif args.mode == "hybrid":
        # Try real data first
        real_success = load_real_data()
        
        # If real data failed or we don't have enough, load mock data
        if not real_success or not check_data_exists():
            print("\n" + "="*60)
            print("Falling back to mock data for reliability...")
            print("="*60)
            load_mock_data()
    
    # Optionally load local datasets
    if args.include_local:
        load_local_datasets()
    
    # Final status check
    print("\n" + "="*60)
    print("Final Status:")
    print("="*60)
    check_data_exists()
    
    print("\n" + "="*60)
    print("✓ Demo preparation complete!")
    print("="*60)
    print("\nYour Horizon platform is ready for presentation.")
    print("Start your servers and visit http://localhost:3000")
    print("\n")


if __name__ == "__main__":
    main()

