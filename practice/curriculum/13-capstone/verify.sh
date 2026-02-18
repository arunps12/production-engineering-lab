#!/bin/bash
# =============================================================================
# Capstone — Verification Script
# Guide: docs/curriculum/13-capstone-project.md
#
# Run this script to verify your capstone project is complete.
# =============================================================================

set -e

echo "=== Capstone Verification ==="

# 1. Check project structure
echo "Checking project structure..."
for f in pyproject.toml Dockerfile docker-compose.yml \
         src/appcore/api/app.py src/appcore/api/routes.py \
         src/appcore/api/schemas.py src/appcore/api/dependencies.py \
         src/appcore/models/predict.py src/appcore/monitoring/metrics.py \
         tests/test_health.py tests/test_predict.py tests/test_metrics.py; do
    if [ ! -f "$f" ]; then
        echo "  MISSING: $f"
    else
        echo "  OK: $f"
    fi
done

# 2. Run tests
echo ""
echo "Running tests..."
# TODO: uv run pytest tests/ -v

# 3. Run linter
echo ""
echo "Running linter..."
# TODO: uv run ruff check src/ tests/

# 4. Build Docker image
echo ""
echo "Building Docker image..."
# TODO: docker build -t practical-production-service .

# 5. Start stack
echo ""
echo "Starting full stack..."
# TODO: docker compose up -d

# 6. Health check
echo ""
echo "Checking health..."
# TODO: sleep 5 && curl -f http://localhost:8000/health

# 7. Metrics check
echo ""
echo "Checking metrics..."
# TODO: curl -s http://localhost:8000/metrics | head -5

echo ""
echo "=== Verification Complete ==="
