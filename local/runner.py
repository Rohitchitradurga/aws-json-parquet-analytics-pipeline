import json
import uuid
import random
import time
import os
import shutil
from datetime import datetime, timezone

# Configuration
LANDING_DIR = "./data/landing"
CLEAN_DIR = "./data/clean"
BATCH_SIZE = 1000

def setup_dirs():
    """Ensure local directories exist."""
    os.makedirs(LANDING_DIR, exist_ok=True)
    os.makedirs(CLEAN_DIR, exist_ok=True)
    print(f"Directories ready: {LANDING_DIR}, {CLEAN_DIR}")

def generate_event():
    """Generate a single fake log event."""
    event_types = ["login", "purchase", "pageview", "error", "logout"]
    users = [f"user_{i}" for i in range(1, 20)]
    
    return {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": random.choice(event_types),
        "user_id": random.choice(users),
        "device_os": random.choice(["ios", "android", "web", "linux"]),
        "session_duration": random.randint(0, 300),
        "meta": {
            "version": "1.0.0",
            "region": random.choice(["us-east-1", "eu-west-1"])
        }
    }

def generate_batch(filename):
    """Generate a batch of NDJSON logs."""
    filepath = os.path.join(LANDING_DIR, filename)
    print(f"Generating {BATCH_SIZE} events to {filepath}...")
    
    with open(filepath, "w") as f:
        for _ in range(BATCH_SIZE):
            event = generate_event()
            f.write(json.dumps(event) + "\n")
    
    print("Generation complete.")
    return filepath

def run_transformation(input_path):
    """
    Simulate triggering the transformation service.
    In a real AWS setup, this would be a Lambda triggered by S3.
    Locally, we just import the function.
    """
    print(f"Triggering transformation for {input_path}")
    
    # Dynamic import to avoid module locking issues if we run this long-term
    from services.transform.main import process_file
    
    try:
        process_file(input_path, CLEAN_DIR)
        print("Transformation successful.")
    except Exception as e:
        print(f"Transformation failed: {e}")

def main():
    setup_dirs()
    
    # 1. Generate Data
    timestamp = int(time.time())
    filename = f"logs_{timestamp}.ndjson"
    
    input_path = generate_batch(filename)
    
    # 2. Transform Data
    # We need to make sure the services module is in the path
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    
    # 3. Load Data (Layer 2)
    print("\n--- Starting Layer 2: Loading ---")

    # Orchestrating properly
    # Re-importing inside main to avoid scope issues
    from services.transform.main import process_file
    from services.loader.postgres_loader import init_db as init_pg, load_parquet_to_postgres
    from services.loader.opensearch_loader import init_index as init_os, load_parquet_to_opensearch
    
    # Init Stores
    print("Initializing Data Stores...")
    init_pg()
    init_os()

    # Transform -> Load
    try:
        # process_file returns the output path now
        parquet_path = process_file(input_path, CLEAN_DIR)
        print("Transformation successful.")
        
        # Loaders
        if parquet_path:
            load_parquet_to_postgres(parquet_path)
            load_parquet_to_opensearch(parquet_path)
            
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
