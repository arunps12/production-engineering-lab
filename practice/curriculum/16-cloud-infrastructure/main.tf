# Exercise 11.B.4 — First Terraform Configuration
# Guide: docs/curriculum/16-cloud-infrastructure-basics.md
# Practice with local provider (no cloud account needed)

# TODO: Uncomment and run: terraform init && terraform plan && terraform apply

# terraform {
#   required_providers {
#     local = {
#       source = "hashicorp/local"
#     }
#   }
# }
#
# resource "local_file" "hello" {
#   content  = "Hello from Terraform!"
#   filename = "${path.module}/hello.txt"
# }
#
# output "file_path" {
#   value = local_file.hello.filename
# }
