#!/bin/bash
# =============================================================================
# Section 5 — Docker: Advanced Debug Lab (D1-D6) + Production (E1)
# Guide: docs/curriculum/05-docker-containerization.md
# =============================================================================

# Exercise 5.D.1 — Container Exits Immediately
# Symptom: docker run myapp exits with code 0/1 immediately
# TODO: Debug with:
# docker logs <container>
# docker run -it myapp bash
# Check CMD vs ENTRYPOINT, check if process crashes

# Exercise 5.D.2 — Image Too Large
# Symptom: Image is 1.2GB when it should be ~200MB
# TODO: Diagnose with:
# docker images
# docker history myimage
# Fix: Use slim base, multi-stage build, .dockerignore, combine RUN layers

# Exercise 5.D.3 — Port Not Accessible
# Symptom: App runs inside container but curl from host fails
# TODO: Check:
# docker ps  (port mapping correct?)
# Does app bind to 0.0.0.0 (not 127.0.0.1)?
# Is EXPOSE in Dockerfile? (informational only)
# Firewall rules?

# Exercise 5.D.4 — Build Cache Not Working
# Symptom: Every build re-installs all dependencies
# TODO: Check Dockerfile layer order:
# BAD: COPY . .  then  RUN pip install
# GOOD: COPY requirements.txt .  then  RUN pip install  then  COPY . .

# Exercise 5.D.5 — Environment Variable Not Set
# TODO: Debug with:
# docker exec <container> env
# Check .env file, docker-compose env_file, ENV vs ARG

# Exercise 5.D.6 — Health Check Always Failing
# TODO: Debug with:
# docker inspect --format='{{json .State.Health}}' <container>
# Is curl installed in the container?
# Is the app ready before first check? (use --start-period)

# ---- PART E: Production Simulation ----
# Exercise 5.E.1 — Full Production Docker Setup
# TODO: Build and run the entire stack:
# docker compose up --build
# docker compose ps
# Test: curl http://localhost:8000/health
# Check logs: docker compose logs -f app
# Check metrics: curl http://localhost:9090
# Tear down: docker compose down -v
