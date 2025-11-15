"""
Initialize database with TimescaleDB extension
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def init_timescaledb():
    """Create TimescaleDB extension if it doesn't exist"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Create TimescaleDB extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb;"))
        conn.commit()
        print("TimescaleDB extension created successfully")

if __name__ == "__main__":
    init_timescaledb()

