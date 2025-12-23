resource "aws_dynamodb_table" "hot_analytics" {
  name           = "${var.project_name}-hot-analytics"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "event_id"
  range_key      = "event_timestamp"

  attribute {
    name = "event_id"
    type = "S"
  }

  attribute {
    name = "event_timestamp"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name               = "UserIdIndex"
    hash_key           = "user_id"
    range_key          = "event_timestamp"
    projection_type    = "ALL"
  }

  tags = {
    Name = "HotAnalyticsStore"
  }
}
