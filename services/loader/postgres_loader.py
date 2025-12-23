import os
import boto3
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine, text

# Configuration
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "analytics_db")
DB_USER = os.environ.get("DB_USER", "analytics_user")
DB_PASS = os.environ.get("DB_PASS", "analytics_password")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    return create_engine(DATABASE_URL)

def init_db():
    """Create necessary tables if they don't exist."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS usage_analytics (
                    event_id TEXT PRIMARY KEY,
                    event_timestamp TIMESTAMP,
                    user_id TEXT,
                    event_type TEXT,
                    device_os TEXT,
                    session_duration INTEGER,
                    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()
            print("Postgres table 'usage_analytics' verified.")
    except Exception as e:
        print(f"Failed to initialize Postgres: {e}")

def load_parquet_to_postgres(parquet_path):
    """
    Reads a Parquet file and loads it into Postgres.
    In production, use COPY command for bulk loading. 
    Here we use Pandas for simplicity and demonstration.
    """
    print(f"Loading {parquet_path} into Postgres...")
    
    try:
        # Read Parquet
        df = pd.read_parquet(parquet_path)
        
        # Simple transformation if needed (e.g. flattening meta)
        # We'll just take the top-level columns for the relational table
        columns = ['event_id', 'event_timestamp', 'user_id', 'event_type', 
                   'device_os', 'session_duration']
        
        # Ensure we only try to load columns that exist
        available_cols = [c for c in columns if c in df.columns]
        df_subset = df[available_cols]
        
        # Write to DB
        engine = get_engine()
        # 'append' mode adds new rows
        df_subset.to_sql('usage_analytics', engine, if_exists='append', index=False)
        
        print(f"Successfully loaded {len(df_subset)} rows to Postgres.")
        
    except Exception as e:
        print(f"Error loading to Postgres: {e}")
        raise

# Lambda Handler Support
def lambda_handler(event, context):
    """
    Triggered by S3 Event (ObjectCreated on Clean bucket)
    """
    # ... Implementation similar to transformation service downloading file ...
    # For the reference repo scope, we'll keep the logic centered on the core function
    # to avoid duplicating too much boilerplate in this file unless requested.
    pass
