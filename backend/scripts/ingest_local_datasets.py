"""
Ingest selected local CSV datasets into Horizon's health metrics tables.

This script is additive and does NOT remove or change any existing data
pulling features (OWID, Google Trends, synthetic pipelines, etc.).

Datasets supported (examples from /Users/tylin/Desktop/datasets):
  - hospital-utilization-trends.csv
  - four-quarter-summary-hospital-utilization-operating-revenue-and-profit-margins.csv
  - monthly-share-of-influenza-tests-that-were-positive.csv

Configure the datasets directory via the LOCAL_DATASETS_DIR environment variable
or place CSV files in a 'datasets' folder at the project root.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import pandas as pd
from sqlalchemy.orm import Session

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import SessionLocal  # noqa: E402
from app.models.health_metrics import HospitalUtilization  # noqa: E402


def get_datasets_dir() -> Path:
  """Resolve the local datasets directory."""
  env_path = os.getenv("LOCAL_DATASETS_DIR")
  if env_path:
      return Path(env_path)
  # Fallback: ../datasets relative to project root (backend/..)
  return backend_dir.parent / "datasets"


def parse_month_year(value: str) -> Optional[datetime]:
  """Parse strings like 'Jan-18' into a datetime at the start of the month."""
  if not value or not isinstance(value, str):
      return None
  try:
      dt = datetime.strptime(value.strip(), "%b-%y")
      # Assume naive dates are in UTC
      return dt.replace(tzinfo=timezone.utc)
  except Exception:
      return None


def ingest_hospital_utilization_trends(csv_path: Path, db: Session) -> None:
  """
  Ingest hospital-utilization-trends.csv into HospitalUtilization.

  Columns: Setting,System,Facility Name,Date,Count
  We map:
    - region_id: 'US-CA' (dataset is California-specific; can be refined later)
    - facility_id: Facility Name
    - metric_type: setting-specific count, e.g. 'ambulatory_surgery_volume'
    - value: Count
    - unit: 'count'
    - timestamp: parsed month/year
  """
  if not csv_path.exists():
      print(f"  - Skipping (file not found): {csv_path}")
      return

  print(f"  - Ingesting hospital utilization trends from {csv_path.name}...")
  df = pd.read_csv(csv_path)

  ingested = 0
  for _, row in df.iterrows():
      setting = str(row.get("Setting", "")).strip()
      facility_name = str(row.get("Facility Name", "")).strip()
      date_str = row.get("Date")
      count = row.get("Count")

      ts = parse_month_year(date_str)
      if ts is None:
          continue

      try:
          value = float(count)
      except Exception:
          continue

      metric_type = f"{setting.lower().replace(' ', '_')}_volume" if setting else "utilization_volume"

      record = HospitalUtilization(
          tenant_id=None,
          region_id="US-CA",
          facility_id=facility_name or None,
          metric_type=metric_type,
          value=value,
          unit="count",
          timestamp=ts,
      )
      db.merge(record)
      ingested += 1

  db.commit()
  print(f"    ✓ Ingested {len(df)} rows ({ingested} valid HospitalUtilization records)")


def ingest_hospital_financials(csv_path: Path, db: Session) -> None:
  """
  Ingest four-quarter-summary-hospital-utilization-operating-revenue-and-profit-margins.csv
  into HospitalUtilization to provide cost/financial context.

  Columns include: Year, Facility Name, Total Margin, Operating Margin, etc.
  We map:
    - region_id: 'US-CA' (dataset is California OSHPD)
    - facility_id: Facility Name
    - metric_type: 'operating_margin' and 'total_margin'
    - value: margin as float (percentage without the '%' sign)
    - unit: 'percentage'
    - timestamp: Jan 1 of the given Year
  """
  if not csv_path.exists():
      print(f"  - Skipping (file not found): {csv_path}")
      return

  print(f"  - Ingesting hospital financial metrics from {csv_path.name}...")
  df = pd.read_csv(csv_path)

  def parse_margin(m: str) -> Optional[float]:
      if not isinstance(m, str):
          return None
      txt = m.strip().replace("%", "")
      if not txt:
          return None
      try:
          return float(txt)
      except Exception:
          return None

  ingested = 0
  for _, row in df.iterrows():
      year = row.get("Year")
      facility_name = str(row.get("Facility Name", "")).strip()
      total_margin = parse_margin(str(row.get("Total Margin", "")))
      operating_margin = parse_margin(str(row.get("Operating Margin", "")))

      try:
          year_int = int(year)
      except Exception:
          continue

      ts = datetime(year_int, 1, 1, tzinfo=timezone.utc)

      for metric_type, margin_value in [
          ("total_margin", total_margin),
          ("operating_margin", operating_margin),
      ]:
          if margin_value is None:
              continue

          record = HospitalUtilization(
              tenant_id=None,
              region_id="US-CA",
              facility_id=facility_name or None,
              metric_type=metric_type,
              value=margin_value,
              unit="percentage",
              timestamp=ts,
          )
          db.merge(record)
          ingested += 1

  db.commit()
  print(f"    ✓ Ingested {ingested} hospital financial metric records")


def ingest_influenza_positivity(csv_path: Path, db: Session) -> None:
  """
  Ingest monthly-share-of-influenza-tests-that-were-positive.csv into HospitalUtilization
  as a generic 'flu_test_positive_share' metric by country.

  Columns: Entity, Day, pcnt_poscombined
  We map:
    - region_id: Entity (country name string)
    - facility_id: None
    - metric_type: 'flu_test_positive_share'
    - value: pcnt_poscombined
    - unit: 'percentage'
    - timestamp: parsed Day
  """
  if not csv_path.exists():
      print(f"  - Skipping (file not found): {csv_path}")
      return

  print(f"  - Ingesting influenza positivity metrics from {csv_path.name}...")
  df = pd.read_csv(csv_path)

  ingested = 0
  for _, row in df.iterrows():
      entity = str(row.get("Entity", "")).strip()
      day = row.get("Day")
      value = row.get("pcnt_poscombined")

      if not entity:
          continue

      try:
          ts = datetime.fromisoformat(str(day)).replace(tzinfo=timezone.utc)
      except Exception:
          continue

      try:
          v = float(value)
      except Exception:
          continue

      record = HospitalUtilization(
          tenant_id=None,
          region_id=entity,
          facility_id=None,
          metric_type="flu_test_positive_share",
          value=v,
          unit="percentage",
          timestamp=ts,
      )
      db.merge(record)
      ingested += 1

  db.commit()
  print(f"    ✓ Ingested {ingested} influenza positivity records")


def main() -> None:
  datasets_dir = get_datasets_dir()
  print(f"\nHORIZON - Ingesting local CSV datasets from: {datasets_dir}\n")

  db: Session = SessionLocal()
  try:
      ingest_hospital_utilization_trends(
          datasets_dir / "hospital-utilization-trends.csv", db
      )
      ingest_hospital_financials(
          datasets_dir
          / "four-quarter-summary-hospital-utilization-operating-revenue-and-profit-margins.csv",
          db,
      )
      ingest_influenza_positivity(
          datasets_dir / "monthly-share-of-influenza-tests-that-were-positive.csv", db
      )
  finally:
      db.close()

  print("\n✓ Local dataset ingestion complete.\n")


if __name__ == "__main__":
  main()


