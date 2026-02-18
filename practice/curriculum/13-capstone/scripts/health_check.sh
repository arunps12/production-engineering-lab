#!/bin/bash
# =============================================================================
# Section 11 — Deployment Health Check Script
# Guide: docs/curriculum/13-capstone-project.md
#
# Exercise: Write a health check script for post-deployment verification.
#
# TODO:
# 1. Define BASE_URL (default http://localhost)
# 2. Define MAX_RETRIES and RETRY_DELAY
# 3. Check /health endpoint with retries
# 4. Check /nginx-health
# 5. Check /metrics
# 6. Print summary (pass/fail count)
# =============================================================================

set -euo pipefail

BASE_URL="${1:-http://localhost}"
MAX_RETRIES=5
RETRY_DELAY=3

echo "Health Check — $BASE_URL"
echo "========================="

# TODO: Implement retry loop for /health
# for i in $(seq 1 $MAX_RETRIES); do
#     if curl -sf "$BASE_URL/health" > /dev/null; then
#         echo "✓ /health is up (attempt $i)"
#         break
#     fi
#     echo "  Waiting... (attempt $i/$MAX_RETRIES)"
#     sleep $RETRY_DELAY
# done

# TODO: Check /nginx-health
# curl -sf "$BASE_URL/nginx-health" > /dev/null && echo "✓ /nginx-health" || echo "✗ /nginx-health"

# TODO: Check /metrics
# curl -sf "$BASE_URL:8000/metrics" > /dev/null && echo "✓ /metrics" || echo "✗ /metrics"

echo ""
echo "Health check complete."
