#!/bin/bash
set -e

echo "Deploying AWS JSON Parquet Analytics Pipeline..."

# 1. Package Lambda
echo "Packaging Lambda..."
# Terraform handles this via archive_file, but in CI we might do it explicitly

# 2. Terraform Apply
echo "Running Terraform..."
cd infra/terraform
terraform init
terraform plan -out=tfplan
# terraform apply tfplan

echo "Deployment Dry-Run Complete."
