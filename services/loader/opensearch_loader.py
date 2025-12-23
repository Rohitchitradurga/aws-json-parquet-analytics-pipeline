import os
import boto3
import pandas as pd
from opensearchpy import OpenSearch, helpers

# Configuration
OS_HOST = os.environ.get("OS_HOST", "127.0.0.1")
OS_PORT = os.environ.get("OS_PORT", "9200")
OS_AUTH = (os.environ.get("OS_USER", "admin"), os.environ.get("OS_PASS", "StrongPassword123!"))
INDEX_NAME = "app-logs"

def get_client():
    # In production/AWS, use AWSV4SignerAuth
    return OpenSearch(
        hosts=[{'host': OS_HOST, 'port': int(OS_PORT)}],
        http_auth=OS_AUTH,
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False
    )

def init_index():
    client = get_client()
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(index=INDEX_NAME, body={
            "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            "mappings": {
                "properties": {
                    "event_timestamp": {"type": "date"},
                    "user_id": {"type": "keyword"},
                    "event_type": {"type": "keyword"},
                    "meta": {"type": "object"}
                }
            }
        })
        print(f"OpenSearch index '{INDEX_NAME}' created.")
    else:
        print(f"OpenSearch index '{INDEX_NAME}' exists.")

def load_parquet_to_opensearch(parquet_path):
    print(f"Loading {parquet_path} into OpenSearch...")
    
    try:
        df = pd.read_parquet(parquet_path)
        client = get_client()
        
        # Convert to dictionary records
        # Handle timestamp serialization if needed
        records = df.to_dict(orient='records')
        
        def doc_generator(data):
            for doc in data:
                yield {
                    "_index": INDEX_NAME,
                    "_source": doc,
                    "_id": doc.get("event_id") # Deduplication key
                }
        
        success, failed = helpers.bulk(client, doc_generator(records), stats_only=True)
        print(f"OpenSearch load: {success} successes, {failed} failures.")
        
    except Exception as e:
        print(f"Error loading to OpenSearch: {e}")
        # Don't raise in dev to allow pipeline to continue if OS is down
