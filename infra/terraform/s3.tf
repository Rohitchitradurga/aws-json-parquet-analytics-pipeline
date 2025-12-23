resource "aws_s3_bucket" "landing_zone" {
  bucket = "${var.project_name}-landing-zone-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket" "clean_zone" {
  bucket = "${var.project_name}-clean-zone-${data.aws_caller_identity.current.account_id}"
}

# Block Public Access (Best Practice)
resource "aws_s3_bucket_public_access_block" "landing_zone" {
  bucket = aws_s3_bucket.landing_zone.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "clean_zone" {
  bucket = aws_s3_bucket.clean_zone.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Lifecycle Rules (Optional - example of cost management)
resource "aws_s3_bucket_lifecycle_configuration" "landing_zone" {
  bucket = aws_s3_bucket.landing_zone.id

  rule {
    id     = "expire_old_raw_logs"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}
