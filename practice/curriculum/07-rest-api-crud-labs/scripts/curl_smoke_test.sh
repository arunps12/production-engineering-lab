#!/usr/bin/env bash
# Module 17: CRUD API curl smoke test
# Usage: bash scripts/curl_smoke_test.sh [BASE_URL]
set -euo pipefail

BASE="${1:-http://localhost:8000}"
PASS=0
FAIL=0

check() {
    local desc="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "  ✓ $desc (HTTP $actual)"
        PASS=$((PASS + 1))
    else
        echo "  ✗ $desc — expected $expected, got $actual"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== CRUD API Smoke Test ==="
echo "Base URL: $BASE"
echo ""

# Health
echo "── Health ──"
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" "$BASE/health")
check "GET /health" "200" "$STATUS"

# Create
echo "── Create ──"
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" -X POST "$BASE/users" \
  -H 'Content-Type: application/json' \
  -d '{"username":"smoketest","email":"smoke@test.com","full_name":"Smoke Test"}')
check "POST /users" "201" "$STATUS"

# List
echo "── List ──"
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" "$BASE/users")
check "GET /users" "200" "$STATUS"

# List with pagination
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" "$BASE/users?page=1&size=2")
check "GET /users?page=1&size=2" "200" "$STATUS"

# Get
echo "── Get ──"
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" "$BASE/users/1")
check "GET /users/1" "200" "$STATUS"

# Get not found
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/users/9999")
check "GET /users/9999 (not found)" "404" "$STATUS"

# PUT
echo "── PUT ──"
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" -X PUT "$BASE/users/1" \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice_put","email":"alice_put@test.com","full_name":"Alice Put"}')
check "PUT /users/1" "200" "$STATUS"

# PATCH
echo "── PATCH ──"
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" -X PATCH "$BASE/users/1" \
  -H 'Content-Type: application/json' \
  -d '{"full_name":"Alice Patched"}')
check "PATCH /users/1" "200" "$STATUS"

# DELETE
echo "── DELETE ──"
STATUS=$(curl -sf -o /dev/null -w "%{http_code}" -X DELETE "$BASE/users/2")
check "DELETE /users/2" "204" "$STATUS"

# DELETE not found
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE/users/2")
check "DELETE /users/2 (already deleted)" "404" "$STATUS"

# Validation error
echo "── Validation ──"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/users" \
  -H 'Content-Type: application/json' \
  -d '{"username":"ab","email":"bad","full_name":""}')
check "POST /users (invalid data)" "422" "$STATUS"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
