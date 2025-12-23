# Services

This directory contains the application code for the pipeline.

## Structure

- **ingestion/**: logic for handling raw data arrival (if needing an API Gateway + Lambda pattern). For S3 triggers, this might be minimal.
- **transform/**: The core conversion logic. Uses `pyarrow` to convert JSON -> Parquet.
- **loader/**: Downstream loaders. These services listen for "Transformation Complete" events (e.g., S3 Event or SNS) and load data into DynamoDB, RDS, etc.
