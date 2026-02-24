#!/bin/bash
# =============================================================================
# Capstone — Verification Script
# Guide: docs/curriculum/20-capstone-project.md
#
# Run this script to verify your capstone project is complete.
# Covers ALL 13 sections of the curriculum.
# =============================================================================

set -e

PASS=0
FAIL=0

check() {
    local desc="$1"
    shift
    if "$@" > /dev/null 2>&1; then
        echo "  ✓ $desc"
        ((PASS++))
    else
        echo "  ✗ $desc"
        ((FAIL++))
    fi
}

echo "=== Capstone Verification ==="
echo ""

# --- Section 0-7: Core Files ---
echo "[Sections 0-7] Core project structure..."
for f in pyproject.toml Dockerfile docker-compose.yml .dockerignore \
         src/appcore/api/app.py src/appcore/api/routes.py \
         src/appcore/api/schemas.py src/appcore/api/dependencies.py \
         src/appcore/api/middleware.py \
         src/appcore/models/predict.py src/appcore/monitoring/metrics.py \
         src/appcore/monitoring/logging.py \
         tests/test_health.py tests/test_predict.py tests/test_metrics.py \
         prometheus.yml; do
    check "$f exists" test -f "$f"
done

# --- Section 13: CI/CD ---
echo ""
echo "[Section 13] CI/CD pipeline..."
check ".github/workflows/ci.yml exists" test -f ".github/workflows/ci.yml"

# --- Section 02: Git ---
echo ""
echo "[Section 02] Git workflow..."
check ".gitignore exists" test -f ".gitignore"
check "Git repository initialized" test -d ".git"
# TODO: check ".git/hooks/pre-commit exists" test -f ".git/hooks/pre-commit"
# TODO: Verify at least one version tag: git tag | grep -q "^v"

# --- Section 04: Database ---
echo ""
echo "[Section 04] Database layer..."
for f in src/appcore/db/__init__.py src/appcore/db/database.py \
         src/appcore/db/repository.py; do
    check "$f exists" test -f "$f"
done
# TODO: check "tests/test_db.py exists" test -f "tests/test_db.py"

# --- Section 11: Security ---
echo ""
echo "[Section 11] Security..."
for f in src/appcore/api/auth.py src/appcore/api/security.py \
         src/appcore/api/rate_limiter.py .env.example; do
    check "$f exists" test -f "$f"
done
# TODO: check "tests/test_auth.py exists" test -f "tests/test_auth.py"

# --- Section 16: Infrastructure ---
echo ""
echo "[Section 16] Infrastructure..."
check "scripts/health_check.sh exists" test -f "scripts/health_check.sh"
check "health_check.sh is executable" test -x "scripts/health_check.sh"
# TODO: check "infra/terraform/main.tf exists" test -f "infra/terraform/main.tf"

# --- Section 12: Nginx ---
echo ""
echo "[Section 12] Nginx reverse proxy..."
check "configs/nginx.conf exists" test -f "configs/nginx.conf"

# --- Build & Runtime Checks ---
echo ""
echo "[Build] Docker build & stack..."
# TODO: Uncomment when ready to test:
# check "Docker image builds" docker build -t practical-production-service .
# check "Stack starts" docker compose up -d
# sleep 5
# check "Health via Nginx (port 80)" curl -sf http://localhost/health
# check "Metrics endpoint" curl -sf http://localhost:8000/metrics
# check "Auth rejects missing key" bash -c '[ "$(curl -s -o /dev/null -w "%{http_code}" http://localhost/predict -X POST -H "Content-Type: application/json" -d "{\"text\":\"test\"}")" = "403" ]'
# check "Nginx health" curl -sf http://localhost/nginx-health
# docker compose down

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && echo "All checks passed!" || echo "Some checks failed — review above."
