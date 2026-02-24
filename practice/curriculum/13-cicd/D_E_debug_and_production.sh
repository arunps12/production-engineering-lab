#!/bin/bash
# =============================================================================
# Section 13 — CI/CD: Advanced Debug Lab (D1-D5) + Production (E1)
# Guide: docs/curriculum/06-cicd-automation.md
# =============================================================================

# Exercise 6.D.1 — CI Passes Locally But Fails in CI
# Symptom: Tests pass on your machine but fail in GitHub Actions
# TODO: Common causes:
# - Different Python version
# - Missing system dependencies
# - Environment variables not set
# - Path differences (Windows vs Linux)
# - Tests depend on order or shared state

# Exercise 6.D.2 — Cache Not Working
# Symptom: CI always installs dependencies from scratch
# TODO: Check cache key, cache path, and restore-keys
# uses: actions/cache@v3
# with:
#   path: ~/.cache/uv
#   key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}

# Exercise 6.D.3 — Docker Build Fails in CI
# Symptom: Docker build works locally but fails in Actions
# TODO: Check:
# - Dockerfile context (are files in .dockerignore?)
# - Base image availability
# - GitHub Actions runner disk space
# - Multi-platform build issues

# Exercise 6.D.4 — Secrets Not Available
# Symptom: Environment variables are empty in CI
# TODO: Check:
# - Secrets added in GitHub Settings → Secrets?
# - Using ${{ secrets.MY_SECRET }} syntax?
# - Secrets not available in fork PRs (security)

# Exercise 6.D.5 — Pipeline Too Slow
# Symptom: CI takes 15+ minutes
# TODO: Optimize:
# - Use caching for dependencies
# - Parallelize jobs (don't chain unnecessarily)
# - Use smaller base images
# - Only run relevant tests (path filters)

# ---- PART E: Production Simulation ----
# Exercise 6.E.1 — Complete CI/CD Pipeline
# TODO: Create the full pipeline by saving C_multistage_pipeline.yml
#       to .github/workflows/ci.yml
# Push to GitHub and verify all stages pass:
# 1. Lint → 2. Test → 3. Build → 4. Deploy
