#!/usr/bin/env bash
# Module 20: Local CI smoke test — validates all practice module services
# Usage: bash scripts/ci_smoke.sh
set -euo pipefail

PASS=0
FAIL=0
CLEANUP_DIRS=()

check() {
    local desc="$1" result="$2"
    if [ "$result" = "0" ]; then
        echo "  ✓ $desc"
        PASS=$((PASS + 1))
    else
        echo "  ✗ $desc"
        FAIL=$((FAIL + 1))
    fi
}

cleanup() {
    echo ""
    echo "=== Cleanup ==="
    for dir in "${CLEANUP_DIRS[@]}"; do
        echo "  Stopping $dir..."
        (cd "$dir" && docker compose down -v 2>/dev/null) || true
    done
    echo "  Done."
}
trap cleanup EXIT

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CURRICULUM="$REPO_ROOT/practice/curriculum"

echo "============================================"
echo "CI Smoke Test — Production Engineering Lab"
echo "============================================"
echo ""

# ── Docker check ──
echo "── Docker ──"
docker info > /dev/null 2>&1
check "Docker is available" $?

# ── Module 14: PostgreSQL ──
echo ""
echo "── Module 14: PostgreSQL ──"
PG_DIR="$CURRICULUM/08-postgresql-production-labs"
if [ -f "$PG_DIR/docker-compose.yml" ]; then
    CLEANUP_DIRS+=("$PG_DIR")
    (cd "$PG_DIR" && docker compose up -d --wait 2>/dev/null)
    sleep 5
    docker compose -f "$PG_DIR/docker-compose.yml" exec -T postgres pg_isready -U labuser -d labdb > /dev/null 2>&1
    check "Postgres is healthy" $?

    docker compose -f "$PG_DIR/docker-compose.yml" exec -T postgres psql -U labuser -d labdb -c "SELECT 1 AS ok" > /dev/null 2>&1
    check "Postgres accepts queries" $?

    docker compose -f "$PG_DIR/docker-compose.yml" exec -T postgres psql -U labuser -d labdb < "$PG_DIR/scripts/schema.sql" > /dev/null 2>&1
    check "Schema creation succeeds" $?

    (cd "$PG_DIR" && docker compose down -v 2>/dev/null)
else
    echo "  SKIP: docker-compose.yml not found"
fi

# ── Module 15: Elasticsearch ──
echo ""
echo "── Module 15: Elasticsearch ──"
ES_DIR="$CURRICULUM/18-elasticsearch-practice"
if [ -f "$ES_DIR/docker-compose.yml" ]; then
    CLEANUP_DIRS+=("$ES_DIR")
    (cd "$ES_DIR" && docker compose up -d es 2>/dev/null)
    echo "  Waiting for ES to start (up to 60s)..."
    for i in $(seq 1 12); do
        if curl -sf http://localhost:9200/_cluster/health > /dev/null 2>&1; then
            break
        fi
        sleep 5
    done
    curl -sf http://localhost:9200/_cluster/health > /dev/null 2>&1
    check "Elasticsearch is healthy" $?

    (cd "$ES_DIR" && docker compose down -v 2>/dev/null)
else
    echo "  SKIP: docker-compose.yml not found"
fi

# ── Module 16: Fuseki ──
echo ""
echo "── Module 16: Fuseki (SPARQL) ──"
FUSEKI_DIR="$CURRICULUM/19-rdf-sparql-labs"
if [ -f "$FUSEKI_DIR/docker-compose.yml" ]; then
    CLEANUP_DIRS+=("$FUSEKI_DIR")
    (cd "$FUSEKI_DIR" && docker compose up -d 2>/dev/null)
    echo "  Waiting for Fuseki to start (up to 30s)..."
    for i in $(seq 1 6); do
        if curl -sf http://localhost:3030/$/ping > /dev/null 2>&1; then
            break
        fi
        sleep 5
    done
    curl -sf http://localhost:3030/$/ping > /dev/null 2>&1
    check "Fuseki is healthy" $?

    (cd "$FUSEKI_DIR" && docker compose down -v 2>/dev/null)
else
    echo "  SKIP: docker-compose.yml not found"
fi

# ── Module 17: CRUD API Tests ──
echo ""
echo "── Module 17: CRUD API Tests ──"
CRUD_DIR="$CURRICULUM/07-rest-api-crud-labs"
if [ -f "$CRUD_DIR/pyproject.toml" ]; then
    (cd "$CRUD_DIR" && uv sync --quiet 2>/dev/null && uv run pytest tests/ -v --tb=short 2>&1 | tail -20)
    check "CRUD API tests pass" $?
else
    echo "  SKIP: pyproject.toml not found"
fi

# ── Summary ──
echo ""
echo "============================================"
echo "Results: $PASS passed, $FAIL failed"
echo "============================================"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
