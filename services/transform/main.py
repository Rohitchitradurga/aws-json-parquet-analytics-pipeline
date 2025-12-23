import pyarrow as pa
import pyarrow.json as pj
import pyarrow.parquet as pq
import os
import json
import boto3
import shutil
from datetime import datetime
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')

def process_file(input_path: str, output_base_dir: str):
    """
    Reads an NDJSON file, converts it to Parquet, and writes it to the output directory
    partitioned by year/month/day.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"Reading {input_path}...")
    
    try:
        # PyaArrow read_json requires a file path or file-like object
        table = pj.read_json(input_path)
    except Exception as e:
        print(f"Error reading JSON with PyArrow: {e}")
        raise

    if table.num_rows == 0:
        print("No records found.")
        return

    # Extract partition info
    try:
        first_timestamp_str = table["event_timestamp"][0].as_py()
        dt = datetime.fromisoformat(first_timestamp_str)
        year, month, day = str(dt.year), str(dt.month).zfill(2), str(dt.day).zfill(2)
    except (KeyError, IndexError, ValueError):
        now = datetime.now()
        year, month, day = str(now.year), str(now.month).zfill(2), str(now.day).zfill(2)

    # Output path construction
    partition_path = os.path.join(output_base_dir, f"year={year}", f"month={month}", f"day={day}")
    os.makedirs(partition_path, exist_ok=True)
    
    basename = os.path.basename(input_path)
    output_filename = basename.replace(".ndjson", ".parquet")
    output_path = os.path.join(partition_path, output_filename)
    
    print(f"Writing parquet to {output_path}...")
    pq.write_table(table, output_path, compression='SNAPPY')
    print(f"Successfully wrote {table.num_rows} rows.")
    return output_path

def lambda_handler(event, context):
    """
    AWS Lambda Handler for S3 Events.
    """
    clean_bucket = os.environ.get('CLEAN_BUCKET')
    if not clean_bucket:
        raise ValueError("CLEAN_BUCKET environment variable is not set")

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        
        print(f"Processing s3://{bucket}/{key}")
        
        # Local processing paths
        tmp_dir = "/tmp"
        local_input_path = os.path.join(tmp_dir, os.path.basename(key))
        local_output_dir = os.path.join(tmp_dir, "output")
        
        # Clean previous run artifacts
        if os.path.exists(local_output_dir):
            shutil.rmtree(local_output_dir)
        os.makedirs(local_output_dir, exist_ok=True)

        try:
            # Download
            s3_client.download_file(bucket, key, local_input_path)
            
            # Transform
            process_file(local_input_path, local_output_dir)
            
            # Upload Result
            # Walk the output directory to find the generated parquet file(s)
            for root, dirs, files in os.walk(local_output_dir):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    # Calculate relative path for S3 key structure (year=.../month=.../...)
                    relative_path = os.path.relpath(local_file_path, local_output_dir)
                    s3_key = relative_path 
                    
                    print(f"Uploading {local_file_path} to s3://{clean_bucket}/{s3_key}")
                    s3_client.upload_file(local_file_path, clean_bucket, s3_key)
            
        except Exception as e:
            print(f"Error processing {key}: {e}")
            raise e
        finally:
            # Cleanup
            if os.path.exists(local_input_path):
                os.remove(local_input_path)
            if os.path.exists(local_output_dir):
                shutil.rmtree(local_output_dir)

    return {"status": "success"}
