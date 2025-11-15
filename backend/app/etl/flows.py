"""
Prefect ETL flows for data ingestion
"""
from prefect import flow, task
from datetime import datetime, timedelta, timezone
import pandas as pd
import requests
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.health_metrics import SearchTrend, PharmacyAggregate, HospitalUtilization, OWIDCovidMetric
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


@task
def fetch_owid_covid_data() -> pd.DataFrame:
    """Fetch Our World in Data COVID metrics"""
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url)
        logger.info(f"Fetched {len(df)} rows from OWID")
        return df
    except Exception as e:
        logger.error(f"Error fetching OWID data: {e}")
        raise


@task
def load_owid_data_to_db(df: pd.DataFrame):
    """Load OWID data into database"""
    db: Session = SessionLocal()
    try:
        # Select relevant columns and convert to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter to recent data (last 90 days)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)
        df_recent = df[df['date'] >= cutoff_date]
        
        for _, row in df_recent.iterrows():
            metric = OWIDCovidMetric(
                location=row.get('location', ''),
                date=row['date'],
                new_cases=row.get('new_cases'),
                new_deaths=row.get('new_deaths'),
                hosp_patients=row.get('hosp_patients'),
                icu_patients=row.get('icu_patients'),
                tests_per_thousand=row.get('tests_per_thousand')
            )
            db.merge(metric)
        
        db.commit()
        logger.info(f"Loaded {len(df_recent)} OWID records to database")
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading OWID data: {e}")
        raise
    finally:
        db.close()


@task
def fetch_google_trends(regions: List[str], keywords: List[str]) -> List[Dict]:
    """Fetch Google Trends data (simplified - in production use pytrends)"""
    # This is a placeholder - in production, use pytrends library
    logger.info(f"Fetching Google Trends for {len(regions)} regions and {len(keywords)} keywords")
    
    # Simulated data for now
    trends = []
    for region in regions:
        for keyword in keywords:
            trends.append({
                'region_id': region,
                'keyword': keyword,
                'search_index': 50.0,  # Placeholder
                'timestamp': datetime.now(timezone.utc)
            })
    
    return trends


@task
def load_search_trends_to_db(trends: List[Dict]):
    """Load search trends into database"""
    db: Session = SessionLocal()
    try:
        for trend in trends:
            search_trend = SearchTrend(
                region_id=trend['region_id'],
                keyword=trend['keyword'],
                search_index=trend['search_index'],
                timestamp=trend['timestamp']
            )
            db.merge(search_trend)
        
        db.commit()
        logger.info(f"Loaded {len(trends)} search trend records")
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading search trends: {e}")
        raise
    finally:
        db.close()


@task
def generate_synthetic_pharmacy_data(regions: List[str]) -> List[Dict]:
    """Generate synthetic pharmacy data for testing"""
    import random
    
    data = []
    for region in regions:
        for drug_category in ['antipyretics', 'cough_suppressants', 'antivirals']:
            data.append({
                'region_id': region,
                'drug_category': drug_category,
                'count': random.randint(100, 1000),
                'timestamp': datetime.now(timezone.utc) - timedelta(hours=random.randint(0, 24))
            })
    
    return data


@task
def load_pharmacy_data_to_db(data: List[Dict]):
    """Load pharmacy aggregates into database"""
    db: Session = SessionLocal()
    try:
        for item in data:
            pharmacy = PharmacyAggregate(
                region_id=item['region_id'],
                drug_category=item['drug_category'],
                count=item['count'],
                timestamp=item['timestamp']
            )
            db.merge(pharmacy)
        
        db.commit()
        logger.info(f"Loaded {len(data)} pharmacy records")
    except Exception as e:
        db.rollback()
        logger.error(f"Error loading pharmacy data: {e}")
        raise
    finally:
        db.close()


@flow(name="ingest_public_data")
def ingest_public_data_flow():
    """Main flow for ingesting public data sources"""
    logger.info("Starting public data ingestion flow")
    
    # Fetch and load OWID data
    try:
        owid_df = fetch_owid_covid_data()
        load_owid_data_to_db(owid_df)
    except Exception as e:
        logger.error(f"OWID ingestion failed: {e}")
    
    # Fetch and load Google Trends
    regions = ['US-CA', 'US-NY', 'US-TX', 'US-FL']
    keywords = ['fever', 'cough', 'flu symptoms', 'shortness of breath']
    
    try:
        trends = fetch_google_trends(regions, keywords)
        load_search_trends_to_db(trends)
    except Exception as e:
        logger.error(f"Google Trends ingestion failed: {e}")
    
    logger.info("Public data ingestion flow completed")


@flow(name="ingest_synthetic_data")
def ingest_synthetic_data_flow():
    """Flow for ingesting synthetic/test data"""
    logger.info("Starting synthetic data ingestion flow")
    
    regions = ['US-CA', 'US-NY', 'US-TX', 'US-FL', 'US-IL']
    
    try:
        pharmacy_data = generate_synthetic_pharmacy_data(regions)
        load_pharmacy_data_to_db(pharmacy_data)
    except Exception as e:
        logger.error(f"Synthetic data ingestion failed: {e}")
    
    logger.info("Synthetic data ingestion flow completed")


if __name__ == "__main__":
    # Run flows locally for testing
    ingest_public_data_flow()
    ingest_synthetic_data_flow()

