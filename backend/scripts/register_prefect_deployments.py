"""
Register Prefect deployments with schedules for Horizon ETL flows.

This script creates a scheduled deployment for the `ingest_public_data_flow`
so that OWID + Google Trends data are ingested automatically on a cadence.
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from app.etl.flows import ingest_public_data_flow


def register_public_data_deployment() -> None:
    """
    Build and apply a Prefect deployment for ingest_public_data_flow.

    Default schedule: hourly (top of the hour) in UTC.
    Adjust the cron string if you want a different cadence.
    """
    deployment = Deployment.build_from_flow(
        flow=ingest_public_data_flow,
        name="ingest-public-data-hourly",
        schedule=CronSchedule(cron="0 * * * *", timezone="UTC"),
        tags=["horizon", "data-ingestion", "public"],
    )
    deployment.apply()


if __name__ == "__main__":
    print("Registering Prefect deployment for ingest_public_data_flow (hourly)...")
    register_public_data_deployment()
    print("✓ Prefect deployment registered.")
    print("Make sure a Prefect agent is running to execute flows on schedule.")


