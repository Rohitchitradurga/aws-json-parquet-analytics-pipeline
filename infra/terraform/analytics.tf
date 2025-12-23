# --------------------------------------------------------------------------------------------------
# Layer 2: Analytics Stores (Optional / Commmented out for cost safety)
# Uncomment these blocks to provision real RDS Postgres and OpenSearch clusters.
# --------------------------------------------------------------------------------------------------

# resource "aws_db_instance" "analytics_postgres" {
#   identifier             = "${var.project_name}-postgres"
#   instance_class         = "db.t3.micro"
#   allocated_storage      = 20
#   engine                 = "postgres"
#   engine_version         = "15.4"
#   username               = "analytics_user"
#   password               = "ChangeMeInProd123!" # Use Secrets Manager in real life
#   db_name                = "analytics_db"
#   publicly_accessible    = false
#   skip_final_snapshot    = true
# }

# resource "aws_opensearch_domain" "analytics_search" {
#   domain_name    = "${var.project_name}-search"
#   engine_version = "OpenSearch_2.11"
#
#   cluster_config {
#     instance_type = "t3.small.search"
#     instance_count = 1
#   }
#
#   ebs_options {
#     ebs_enabled = true
#     volume_size = 10
#   }
# }
