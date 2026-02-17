# SECTION 8 — FINAL CAPSTONE PROJECT

---

## Overview

This capstone combines **every skill** from the curriculum into one integrated project. You will build, containerize, test, deploy, and monitor `practical-production-service` from scratch — just like you would on your first week at a real engineering team.

**What you're building:** A production-grade prediction API with:
- Python project managed by `uv` (Section 0)
- Linux process management and debugging (Section 1)
- Network configuration and troubleshooting (Section 2)
- Clean REST API design (Section 3)
- FastAPI implementation with middleware, DI, tests (Section 4)
- Docker containerization with multi-stage builds (Section 5)
- CI/CD pipeline with GitHub Actions (Section 6)
- Prometheus monitoring and structured logging (Section 7)

**Three difficulty levels:**
- **Level 1 — Guided:** Step-by-step instructions. Follow them exactly.
- **Level 2 — Semi-guided:** High-level requirements. You decide the implementation.
- **Level 3 — Production simulation:** Realistic scenario with ambiguous requirements and things that break.

---

## LEVEL 1 — GUIDED CAPSTONE

### Step 1: Initialize the Project (Section 0)

```bash
mkdir -p ~/Projects/practical-production-service
cd ~/Projects/practical-production-service

# Initialize with uv
uv init --lib --name appcore

# Set Python version
echo "3.11" > .python-version

# Add all dependencies
uv add fastapi uvicorn pydantic prometheus_client
uv add --dev pytest httpx ruff

# Verify lockfile and venv
ls uv.lock .venv/bin/python
uv run python --version
```

**Checkpoint:**
```bash
# All must pass:
test -f pyproject.toml && echo "✓ pyproject.toml exists"
test -f uv.lock && echo "✓ uv.lock exists"
test -d .venv && echo "✓ .venv exists"
uv run python -c "import fastapi; print(f'✓ FastAPI {fastapi.__version__}')"
uv run python -c "import prometheus_client; print(f'✓ prometheus_client {prometheus_client.__version__}')"
```

### Step 2: Create the Project Structure (Sections 0, 3, 4)

```bash
mkdir -p src/appcore/api
mkdir -p src/appcore/models
mkdir -p src/appcore/monitoring
mkdir -p tests
mkdir -p configs
```

```python
# src/appcore/__init__.py
__version__ = "0.1.0"
```

```python
# src/appcore/models/__init__.py
```

```python
# src/appcore/models/predict.py
from typing import Protocol

class PredictionModel(Protocol):
    version: str
    def predict(self, features: list[float]) -> float: ...
    def is_healthy(self) -> bool: ...


class SimplePredictionModel:
    """Simple model that returns the mean of features."""
    
    def __init__(self, version: str = "v1.0"):
        self.version = version
        self._loaded = True
    
    def predict(self, features: list[float]) -> float:
        if not features:
            raise ValueError("Features list cannot be empty")
        return sum(features) / len(features)
    
    def is_healthy(self) -> bool:
        return self._loaded
```

```python
# src/appcore/api/__init__.py
```

```python
# src/appcore/api/schemas.py
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: list[float] = Field(..., min_length=1, description="Input features for prediction")


class PredictResponse(BaseModel):
    prediction_id: str
    result: float
    model_version: str
    created_at: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    checks: dict


class VersionResponse(BaseModel):
    version: str
    api_version: str
    model_version: str
```

```python
# src/appcore/monitoring/__init__.py
```

```python
# src/appcore/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

PREDICTION_COUNT = Counter(
    "predictions_total",
    "Total predictions made",
    ["model_version", "status"],
)

PREDICTION_LATENCY = Histogram(
    "prediction_duration_seconds",
    "Prediction inference duration",
    ["model_version"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.5, 1.0, 5.0],
)

HEALTH_STATUS = Gauge("app_health_status", "Application health (1=healthy, 0=unhealthy)")

APP_INFO = Info("app", "Application metadata")
```

```python
# src/appcore/api/dependencies.py
from functools import lru_cache
from appcore.models.predict import SimplePredictionModel, PredictionModel


@lru_cache(maxsize=1)
def get_model() -> PredictionModel:
    return SimplePredictionModel(version="v1.0")
```

```python
# src/appcore/api/routes.py
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from appcore import __version__
from appcore.api.schemas import (
    PredictRequest,
    PredictResponse,
    HealthResponse,
    VersionResponse,
)
from appcore.api.dependencies import get_model
from appcore.models.predict import PredictionModel
from appcore.monitoring.metrics import (
    PREDICTION_COUNT,
    PREDICTION_LATENCY,
    HEALTH_STATUS,
)

router = APIRouter()

_start_time = time.time()


@router.get("/health", response_model=HealthResponse)
def health_check(model: PredictionModel = Depends(get_model)):
    checks = {
        "model_loaded": model.is_healthy(),
        "uptime_seconds": round(time.time() - _start_time, 2),
    }
    all_healthy = all(checks.values())
    HEALTH_STATUS.set(1 if all_healthy else 0)
    
    if not all_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "unhealthy", "checks": checks},
        )
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        checks=checks,
    )


@router.get("/version", response_model=VersionResponse)
def version(model: PredictionModel = Depends(get_model)):
    return VersionResponse(
        version=__version__,
        api_version="v1",
        model_version=model.version,
    )


@router.post("/predict", response_model=PredictResponse, status_code=status.HTTP_201_CREATED)
def predict(request: PredictRequest, model: PredictionModel = Depends(get_model)):
    start = time.perf_counter()
    try:
        result = model.predict(request.features)
        duration = time.perf_counter() - start
        
        PREDICTION_COUNT.labels(model_version=model.version, status="success").inc()
        PREDICTION_LATENCY.labels(model_version=model.version).observe(duration)
        
        return PredictResponse(
            prediction_id=str(uuid.uuid4()),
            result=result,
            model_version=model.version,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
    except ValueError as e:
        PREDICTION_COUNT.labels(model_version=model.version, status="error").inc()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
```

```python
# src/appcore/api/app.py
import time
import uuid
import json
import logging
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from appcore import __version__
from appcore.api.routes import router
from appcore.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY, APP_INFO


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for attr in ("request_id", "method", "path", "status_code", "duration_ms"):
            if hasattr(record, attr):
                log_data[attr] = getattr(record, attr)
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logging.root.handlers = [handler]
logging.root.setLevel(logging.INFO)

logger = logging.getLogger("appcore")


app = FastAPI(
    title="Practical Production Service",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Prometheus /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

APP_INFO.info({"version": __version__})


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    if request.url.path.startswith("/metrics"):
        return await call_next(request)
    
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()
    
    response = await call_next(request)
    
    duration = time.perf_counter() - start
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)
    
    response.headers["X-Request-ID"] = request_id
    
    logger.info(
        "%s %s → %d (%.3fs)",
        request.method,
        request.url.path,
        response.status_code,
        duration,
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
        },
    )
    
    return response


app.include_router(router)
```

**Checkpoint:**
```bash
uv run uvicorn appcore.api.app:app --port 8000 &
sleep 2
curl -s http://localhost:8000/health | python3 -m json.tool
curl -s http://localhost:8000/version | python3 -m json.tool
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}' | python3 -m json.tool
curl -s http://localhost:8000/metrics | head -20
kill %1
```

### Step 3: Write Tests (Section 4)

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from appcore.api.app import app
from appcore.api.dependencies import get_model
from appcore.models.predict import SimplePredictionModel


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_model():
    return SimplePredictionModel(version="test-v1")
```

```python
# tests/test_health.py
def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "checks" in data
    assert data["checks"]["model_loaded"] is True


def test_health_includes_uptime(client):
    response = client.get("/health")
    data = response.json()
    assert "uptime_seconds" in data["checks"]
    assert data["checks"]["uptime_seconds"] >= 0
```

```python
# tests/test_version.py
def test_version_returns_200(client):
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "api_version" in data
    assert "model_version" in data
```

```python
# tests/test_predict.py
def test_predict_valid_features(client):
    response = client.post("/predict", json={"features": [1.0, 2.0, 3.0]})
    assert response.status_code == 201
    data = response.json()
    assert data["result"] == 2.0  # mean of [1, 2, 3]
    assert "prediction_id" in data
    assert "model_version" in data
    assert "created_at" in data


def test_predict_single_feature(client):
    response = client.post("/predict", json={"features": [5.0]})
    assert response.status_code == 201
    assert response.json()["result"] == 5.0


def test_predict_empty_features_rejected(client):
    response = client.post("/predict", json={"features": []})
    assert response.status_code == 422


def test_predict_missing_features(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_wrong_type(client):
    response = client.post("/predict", json={"features": "not a list"})
    assert response.status_code == 422
```

```python
# tests/test_metrics.py
def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


def test_metrics_count_requests(client):
    client.get("/health")
    client.get("/health")
    response = client.get("/metrics")
    assert 'endpoint="/health"' in response.text


def test_prediction_metrics_recorded(client):
    client.post("/predict", json={"features": [1.0, 2.0]})
    response = client.get("/metrics")
    assert "predictions_total" in response.text
    assert "prediction_duration_seconds" in response.text
```

**Checkpoint:**
```bash
uv run pytest tests/ -v
# All tests must pass

uv run ruff check src/ tests/
# No linting errors
```

### Step 4: Containerize (Section 5)

```dockerfile
# Dockerfile
FROM python:3.11-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev deps in production)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application code
COPY src/ src/
COPY README.md ./

# Install the project itself
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.11-slim AS production

WORKDIR /app

# Copy the venv from build stage
COPY --from=base /app/.venv /app/.venv

# Ensure the venv is on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "appcore.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```
# .dockerignore
.venv/
__pycache__/
*.pyc
.git/
.github/
.ruff_cache/
*.egg-info/
dist/
build/
.pytest_cache/
docs/
```

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_NAME=practical-production-service
      - LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./configs/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    depends_on:
      api:
        condition: service_healthy
    restart: unless-stopped
```

```yaml
# configs/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "practical-production-service"
    static_configs:
      - targets: ["api:8000"]
    metrics_path: "/metrics"
    scrape_interval: 5s
```

**Checkpoint:**
```bash
# Build and verify image
docker build -t practical-production-service:latest .
docker images | grep practical-production-service

# Run and test
docker run -d --name test-api -p 8000:8000 practical-production-service:latest
sleep 3
curl -s http://localhost:8000/health | python3 -m json.tool
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}' | python3 -m json.tool
curl -s http://localhost:8000/metrics | head -10
docker stop test-api && docker rm test-api

# Run full stack
docker compose up -d
sleep 5
curl -s http://localhost:8000/health
curl -s http://localhost:9090/api/v1/targets | python3 -m json.tool | head -10
docker compose down
```

### Step 5: Set Up CI/CD (Section 6)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
      - run: uv sync --frozen
      - run: uv run ruff check src/ tests/
      - run: uv run ruff format --check src/ tests/

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          version: "latest"
      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync --frozen
      - run: uv run pytest tests/ -v --tb=short

  docker:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t practical-production-service:${{ github.sha }} .
      - name: Run smoke test
        run: |
          docker run -d --name smoke-test -p 8000:8000 \
            practical-production-service:${{ github.sha }}
          sleep 5
          curl -f http://localhost:8000/health
          curl -f http://localhost:8000/version
          curl -f -X POST http://localhost:8000/predict \
            -H "Content-Type: application/json" \
            -d '{"features": [1.0, 2.0, 3.0]}'
          docker stop smoke-test
```

**Checkpoint:**
```bash
# Test CI locally
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run pytest tests/ -v
docker build -t practical-production-service:test .
```

### Step 6: Verify Everything Works Together

Run this final verification script:

```bash
#!/bin/bash
# scripts/verify_capstone.sh
set -e

echo "=========================================="
echo "  CAPSTONE VERIFICATION SCRIPT"
echo "=========================================="

PASS=0
FAIL=0

check() {
    if eval "$2" > /dev/null 2>&1; then
        echo "  ✓ $1"
        PASS=$((PASS + 1))
    else
        echo "  ✗ $1"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "--- Section 0: Project Structure ---"
check "pyproject.toml exists" "test -f pyproject.toml"
check "uv.lock exists" "test -f uv.lock"
check ".venv exists" "test -d .venv"
check "src layout correct" "test -f src/appcore/__init__.py"
check "Python imports work" "uv run python -c 'import appcore'"

echo ""
echo "--- Section 1: Linux ---"
check "Can find Python process" "which python3"
check "Port 8000 concept understood" "true"

echo ""
echo "--- Section 3 & 4: API ---"
check "Routes module exists" "test -f src/appcore/api/routes.py"
check "Schemas module exists" "test -f src/appcore/api/schemas.py"
check "App module exists" "test -f src/appcore/api/app.py"

echo ""
echo "--- Section 4: Testing ---"
check "Test files exist" "ls tests/test_*.py"
check "Tests pass" "uv run pytest tests/ -q"
check "Linting passes" "uv run ruff check src/ tests/"

echo ""
echo "--- Section 5: Docker ---"
check "Dockerfile exists" "test -f Dockerfile"
check ".dockerignore exists" "test -f .dockerignore"
check "docker-compose.yml exists" "test -f docker-compose.yml"
check "Image builds" "docker build -t capstone-verify:test . -q"

echo ""
echo "--- Section 6: CI/CD ---"
check "CI workflow exists" "test -f .github/workflows/ci.yml"

echo ""
echo "--- Section 7: Monitoring ---"
check "Metrics module exists" "test -f src/appcore/monitoring/metrics.py"
check "Prometheus config exists" "test -f configs/prometheus.yml"

echo ""
echo "--- Integration: Smoke Test ---"
docker run -d --name capstone-smoke -p 8000:8000 capstone-verify:test > /dev/null 2>&1
sleep 4

check "GET /health returns 200" "curl -sf http://localhost:8000/health"
check "GET /version returns 200" "curl -sf http://localhost:8000/version"
check "POST /predict returns 201" "curl -sf -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d '{\"features\": [1.0, 2.0]}' | grep 201"
check "GET /metrics returns prometheus format" "curl -sf http://localhost:8000/metrics | grep http_requests_total"
check "Invalid request returns 422" "curl -sf -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d '{\"features\": []}' | grep 422"

docker stop capstone-smoke > /dev/null 2>&1 && docker rm capstone-smoke > /dev/null 2>&1

echo ""
echo "=========================================="
echo "  Results: $PASS passed, $FAIL failed"
echo "=========================================="

if [ "$FAIL" -gt 0 ]; then
    echo "  ⚠ Some checks failed. Review and fix."
    exit 1
else
    echo "  🎉 All checks passed! Capstone complete."
fi
```

---

## LEVEL 2 — SEMI-GUIDED CAPSTONE

**You have done Level 1. Now rebuild from scratch with only high-level requirements.**

Delete your project and start over:
```bash
rm -rf ~/Projects/practical-production-service
mkdir ~/Projects/practical-production-service
cd ~/Projects/practical-production-service
```

### Requirements

Build a service called `appcore` that meets these specifications:

**Project (Section 0):**
- Managed entirely with `uv` — no pip
- `src/` layout
- Lock file committed
- Dev dependencies separated from production dependencies

**API (Sections 3, 4):**
- `GET /health` — returns health status with dependency checks, 200 if healthy, 503 if not
- `GET /version` — returns app version, API version, model version
- `POST /predict` — accepts JSON `{"features": [float, ...]}`, returns prediction with ID, result, model version, timestamp
- `GET /metrics` — Prometheus-compatible text format
- All responses use Pydantic models
- Request validation with meaningful error messages
- Request ID tracking via middleware
- Structured JSON logging

**Testing (Section 4):**
- Minimum 10 tests covering all endpoints
- Test happy path AND error cases
- All tests pass with `uv run pytest`

**Docker (Section 5):**
- Multi-stage Dockerfile (build + production stages)
- Non-root user in production stage
- Health check configured
- `docker-compose.yml` with API + Prometheus
- Image size under 200MB

**CI (Section 6):**
- GitHub Actions workflow
- Lint → Test → Docker build pipeline
- Smoke test in CI

**Monitoring (Section 7):**
- Request counter with method, endpoint, status labels
- Request latency histogram
- Prediction counter and latency histogram
- Health gauge
- Prometheus scrape configuration

### Acceptance Criteria

Run the verification script from Level 1. All checks must pass.

### Hints (only if stuck)

<details>
<summary>Hint 1: Project initialization</summary>

```bash
uv init --lib --name appcore
uv add fastapi uvicorn pydantic prometheus_client
uv add --dev pytest httpx ruff
```
</details>

<details>
<summary>Hint 2: Metrics endpoint mount</summary>

```python
from prometheus_client import make_asgi_app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```
</details>

<details>
<summary>Hint 3: Multi-stage Dockerfile</summary>

```dockerfile
FROM python:3.11-slim AS base
# ... build stage with uv sync
FROM python:3.11-slim AS production
# ... copy only .venv from base
```
</details>

---

## LEVEL 3 — PRODUCTION SIMULATION

### Scenario: Week 1 at Your New Job

You just joined a team. There is a legacy service running in production that needs to be modernized. Your tech lead gives you the following requirements.

**The situation:**
- There is an existing "prediction service" running on a VM
- It was set up manually — no Dockerfile, no CI, no monitoring
- Customers are complaining about intermittent errors
- Nobody knows what Python version or dependencies are installed
- The team wants to move to a modern, reproducible setup

**Your assignment:**

> "Hey, welcome to the team! We need you to rebuild our prediction service. Here's what we need:
>
> 1. **Make it reproducible.** Right now, the server was set up by someone who left. We need to be able to rebuild it from scratch. Use that `uv` tool, Docker, the whole thing.
>
> 2. **Make it observable.** We have Prometheus set up but the service doesn't expose metrics. We need at least request counts, latency percentiles, and error rates. I also need JSON logs so our log aggregator can parse them.
>
> 3. **Make it testable.** There are zero tests. Add enough tests that we can confidently deploy changes. Wire it up with GitHub Actions.
>
> 4. **Keep the API contract.** The existing endpoints are `/health`, `/version`, and `/predict`. Don't change the request/response format — other services depend on them.
>
> 5. **Document your decisions.** Write a `DECISIONS.md` file explaining what you chose and why."
>
> No, you can't ask the previous developer. They left a month ago.

### Deliverables

1. **Complete project** with all source code in `src/appcore/`
2. **Dockerfile** with multi-stage build
3. **docker-compose.yml** with API + Prometheus
4. **CI/CD pipeline** (`.github/workflows/ci.yml`)
5. **Tests** with >80% endpoint coverage
6. **DECISIONS.md** explaining:
   - Why you chose `uv` over pip/poetry
   - Why src-layout over flat layout
   - Your Docker strategy (base image, multi-stage rationale, image size)
   - Your monitoring approach (what metrics, why those buckets)
   - Your testing strategy (what you test and why)
7. **README.md** with setup and run instructions

### Challenges You'll Face

These are deliberately vague or ambiguous — just like real requirements:

- "Latency percentiles" — which ones? You decide (and justify in DECISIONS.md)
- "Enough tests" — what's enough? Your call
- "JSON logs so our log aggregator can parse them" — what fields? You figure it out
- "Other services depend on the API" — so you need to test the contract, not just happy path
- "Make it reproducible" — does that include the Prometheus config? The Docker compose? You decide

### How to Evaluate Level 3

**Functional requirements** (must work):
- `docker compose up` starts API + Prometheus
- `curl /health` returns 200
- `curl /predict` with valid features returns 201 with correct schema
- `curl /metrics` returns Prometheus text format
- `uv run pytest` — all tests pass
- `uv run ruff check` — no errors
- CI workflow syntax is valid

**Non-functional requirements** (must be reasonable):
- Docker image under 200MB
- p95 latency under 100ms for `/health`
- p95 latency under 500ms for `/predict`
- Zero test flakiness (run `pytest` 3 times, all pass)

**Decision quality** (DECISIONS.md):
- Each decision has a rationale (not just "because tutorial said so")
- Trade-offs are acknowledged
- Alternatives are mentioned
- Decisions are consistent with each other

---

## Capstone Checklist

Use this checklist to track your progress:

### Core Files
- [ ] `pyproject.toml` — project definition with all dependencies
- [ ] `uv.lock` — locked dependency versions
- [ ] `.python-version` — Python version pin
- [ ] `src/appcore/__init__.py` — package with version
- [ ] `src/appcore/api/app.py` — FastAPI application with middleware
- [ ] `src/appcore/api/routes.py` — endpoint handlers
- [ ] `src/appcore/api/schemas.py` — Pydantic models
- [ ] `src/appcore/api/dependencies.py` — dependency injection
- [ ] `src/appcore/models/predict.py` — prediction model
- [ ] `src/appcore/monitoring/metrics.py` — Prometheus metrics

### Container & Deployment
- [ ] `Dockerfile` — multi-stage, non-root, health check
- [ ] `.dockerignore` — excludes unnecessary files
- [ ] `docker-compose.yml` — API + Prometheus
- [ ] `configs/prometheus.yml` — scrape configuration

### Testing & CI
- [ ] `tests/conftest.py` — shared fixtures
- [ ] `tests/test_health.py` — health endpoint tests
- [ ] `tests/test_version.py` — version endpoint tests
- [ ] `tests/test_predict.py` — prediction tests (valid + invalid)
- [ ] `tests/test_metrics.py` — monitoring tests
- [ ] `.github/workflows/ci.yml` — CI pipeline

### Endpoints
- [ ] `GET /health` → 200 with status, checks, timestamp
- [ ] `GET /version` → 200 with version, api_version, model_version
- [ ] `POST /predict` → 201 with prediction_id, result, model_version, created_at
- [ ] `POST /predict` (invalid) → 422 with error details
- [ ] `GET /metrics` → Prometheus text format with all custom metrics

### Quality
- [ ] All tests pass: `uv run pytest -v`
- [ ] Lint clean: `uv run ruff check src/ tests/`
- [ ] Docker image builds successfully
- [ ] Docker compose brings up API + Prometheus
- [ ] Prometheus can scrape the API metrics

---

## What You've Learned

By completing this capstone, you've demonstrated:

| Section | Skill | Evidence |
|---|---|---|
| 0 | Modern Python packaging | `uv` project with lockfile, reproducible builds |
| 1 | Linux fundamentals | Process management, port debugging, permissions |
| 2 | Networking | Understanding localhost, port binding, DNS in Docker |
| 3 | REST API design | Clean endpoints, proper status codes, validation |
| 4 | FastAPI | Middleware, DI, async, testing with TestClient |
| 5 | Docker | Multi-stage builds, compose, health checks |
| 6 | CI/CD | Automated lint, test, build pipeline |
| 7 | Monitoring | Prometheus metrics, structured logging, observability |

**You can now:**
- Set up a Python project from scratch with reproducible dependencies
- Build a production-quality REST API
- Containerize and deploy it
- Monitor it with metrics and structured logs
- Automate testing and deployment with CI/CD

**This is exactly what production engineering teams do every day.**

---

*Congratulations on completing the curriculum! Return to [README](README.md) for the full learning path overview.*
