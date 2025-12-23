# --------------------------------------------------------------------------------------------------
# Layer 3: Scale (Optional / Commented out)
# --------------------------------------------------------------------------------------------------

# resource "aws_kinesis_stream" "event_stream" {
#   name             = "${var.project_name}-stream"
#   shard_count      = 1
#   retention_period = 24
# }

# resource "aws_glue_job" "batch_processor" {
#   name     = "${var.project_name}-batch-job"
#   role_arn = aws_iam_role.glue_role.arn # Requires Glue role definition
#   command {
#     script_location = "s3://${aws_s3_bucket.landing_zone.bucket}/scripts/glue_etl.py"
#   }
# }
