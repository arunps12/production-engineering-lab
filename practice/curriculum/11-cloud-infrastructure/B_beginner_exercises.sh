#!/bin/bash
# =============================================================================
# Section 11 — Cloud & Infrastructure: Beginner Exercises (B1-B7)
# Guide: docs/curriculum/11-cloud-infrastructure-basics.md
# =============================================================================

# Exercise 11.B.1 — Cloud Mental Model
# TODO: Draw the production deployment diagram
# Internet → DNS → Load Balancer → App Servers → Database/Cache/Storage

# Exercise 11.B.2 — SSH into a Remote Server
# TODO: ssh-keygen -t ed25519 -C "your-email@example.com"
# TODO: ssh-copy-id user@server-ip
# TODO: ssh user@server-ip

# Exercise 11.B.3 — SCP and File Transfer
# TODO: scp local-file.txt user@server:/remote/path/
# TODO: scp user@server:/remote/file.txt ./local/
# TODO: scp -r ./project user@server:/home/user/

# Exercise 11.B.4 — First Terraform Configuration
# TODO: See main.tf in this directory
# terraform init && terraform plan && terraform apply

# Exercise 11.B.5 — Terraform Variables and Outputs
# TODO: See variables.tf in this directory

# Exercise 11.B.6 — Object Storage with MinIO
# TODO: docker run -d -p 9000:9000 -p 9001:9001 \
#   -e MINIO_ROOT_USER=admin \
#   -e MINIO_ROOT_PASSWORD=password \
#   minio/minio server /data --console-address ":9001"

# Exercise 11.B.7 — Environment Parity with Docker
# TODO: docker compose --env-file .env.development up
# TODO: docker compose --env-file .env.production up
