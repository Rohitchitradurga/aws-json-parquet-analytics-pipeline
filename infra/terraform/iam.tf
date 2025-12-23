# Lambda Execution Role
resource "aws_iam_role" "transformer_role" {
  name = "${var.project_name}-transformer-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Basic Lambda Logging Policy
resource "aws_iam_role_policy_attachment" "transformer_basic_execution" {
  role       = aws_iam_role.transformer_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 Access Policy
resource "aws_iam_policy" "transformer_s3_policy" {
  name        = "${var.project_name}-transformer-s3-policy"
  description = "Allow reading from landing and writing to clean buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.landing_zone.arn,
          "${aws_s3_bucket.landing_zone.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:AbortMultipartUpload"
        ]
        Resource = [
          aws_s3_bucket.clean_zone.arn,
          "${aws_s3_bucket.clean_zone.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "transformer_s3_attach" {
  role       = aws_iam_role.transformer_role.name
  policy_arn = aws_iam_policy.transformer_s3_policy.arn
}
