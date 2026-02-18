# =============================================================================
# Section 11 — Infrastructure as Code (Terraform)
# Guide: docs/curriculum/13-capstone-project.md
#
# Exercise (Optional): Use Terraform local provider to generate config files.
#
# TODO:
# 1. Generate docker-compose.yml from template
# 2. Generate .env from template with default values
# 3. Run with: terraform init && terraform apply
# =============================================================================

# terraform {
#   required_providers {
#     local = {
#       source  = "hashicorp/local"
#       version = "~> 2.0"
#     }
#   }
# }
#
# variable "api_key" {
#   description = "API key for the service"
#   type        = string
#   sensitive   = true
#   default     = "dev-key-change-me"
# }
#
# variable "log_level" {
#   description = "Application log level"
#   type        = string
#   default     = "info"
# }
#
# resource "local_file" "env" {
#   filename = "${path.module}/../../.env"
#   content  = <<-EOT
#     API_KEY=${var.api_key}
#     LOG_LEVEL=${var.log_level}
#     DATABASE_URL=sqlite:///data/predictions.db
#     REDIS_URL=redis://redis:6379/0
#   EOT
# }
