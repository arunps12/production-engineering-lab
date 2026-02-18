#!/bin/bash
# =============================================================================
# Section 9 — Database: Docker Commands (B4-B6) + Production (E1)
# Guide: docs/curriculum/09-database-fundamentals.md
# =============================================================================

# Exercise 9.B.4 — PostgreSQL with Docker
# TODO: docker run -d --name postgres \
#   -e POSTGRES_PASSWORD=secret \
#   -e POSTGRES_DB=practice \
#   -p 5432:5432 \
#   postgres:16
# TODO: docker exec -it postgres psql -U postgres -d practice

# Exercise 9.B.5 — Redis Basics
# TODO: docker run -d --name redis -p 6379:6379 redis:7
# TODO: docker exec -it redis redis-cli
# SET, GET, SETEX, TTL, DEL, INCR

# Exercise 9.C.6 — Backup and Restore
# TODO: docker exec postgres pg_dump -U postgres practice > backup.sql
# TODO: docker exec -i postgres psql -U postgres practice < backup.sql

# Exercise 9.C.7 — Docker Compose with Database
# TODO: See docker-compose.yml in this directory

# --- PRODUCTION ---
# Exercise 9.E.1 — Full Database Stack
# TODO: docker compose up --build
# TODO: Run migrations
# TODO: Test caching with Redis
# TODO: Test rate limiting
# TODO: Verify backups work
