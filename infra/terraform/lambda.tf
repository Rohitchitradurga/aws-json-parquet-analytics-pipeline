data "archive_file" "transformer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../services/transform"
  output_path = "${path.module}/transformer.zip"
  excludes    = ["__pycache__", ".DS_Store"]
}

resource "aws_lambda_function" "transformer" {
  filename      = data.archive_file.transformer_zip.output_path
  function_name = "${var.project_name}-transformer"
  role          = aws_iam_role.transformer_role.arn
  handler       = "main.process_file" # Note: main.py needs a lambda_handler wrapper, checking that next.
  source_code_hash = data.archive_file.transformer_zip.output_base64sha256
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 512

  environment {
    variables = {
      CLEAN_BUCKET = aws_s3_bucket.clean_zone.id
    }
  }

  lifecycle {
    ignore_changes = [filename] # Ignore code changes for terraform, assume CI/CD handles it or manual update
  }
}

# S3 Trigger
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transformer.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.landing_zone.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.landing_zone.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.transformer.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".ndjson"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}
