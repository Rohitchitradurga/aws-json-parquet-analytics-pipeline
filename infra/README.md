# Infrastructure

This directory contains the Terraform code to provision the AWS environment.

## Modules

- **s3**: Landing and Clean buckets.
- **lambda**: Transformation and Loader functions.
- **dynamodb**: Hot store table definitions.
- **rds**: Postgres instance (optional).
- **opensearch**: OpenSearch domain (optional).

## Usage

```bash
cd terraform
terraform init
terraform plan
terraform apply
```
