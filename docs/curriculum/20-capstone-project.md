# SECTION 20 — FINAL CAPSTONE PROJECT

---

## Overview

This capstone combines **every skill** from the curriculum into one integrated project. You will build, containerize, test, deploy, and monitor `practical-production-service` from scratch — just like you would on your first week at a real engineering team.

**What you're building:** A production-grade prediction API with:
- Python project managed by `uv` (Section 0)
- Linux process management and debugging (Section 1)
- Network configuration and troubleshooting (Section 03)
- Clean REST API design (Section 05)
- FastAPI implementation with middleware, DI, tests (Section 06)
- Docker containerization with multi-stage builds (Section 09)
- CI/CD pipeline with GitHub Actions (Section 13)
- Prometheus monitoring and structured logging (Section 15)
- Git workflow with branching, hooks, and tags (Section 02)
- Database integration with SQLite/PostgreSQL and Redis caching (Section 04)
- Security hardening — JWT auth, secrets management, input validation (Section 11)
- Infrastructure as Code with Terraform and health checks (Section 16)
- Nginx reverse proxy with load balancing and SSL (Section 12)

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

### Step 2: Create the Project Structure (Sections 0, 5, 6)

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

### Step 3: Write Tests (Section 06)

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

### Step 4: Containerize (Section 09)

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

### Step 5: Set Up CI/CD (Section 13)

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

### Step 7: Set Up Git Workflow (Section 02)

```bash
cd ~/Projects/practical-production-service

# Initialize Git repository
git init
git branch -M main

# Create a proper .gitignore
cat > .gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
*.egg-info/
dist/
build/
.env
*.db
*.sqlite3
EOF

# Initial commit
git add -A
git commit -m "feat: initial project structure with API and monitoring"

# Create a pre-commit hook for linting
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
echo "Running pre-commit checks..."
uv run ruff check src/ tests/ || exit 1
uv run ruff format --check src/ tests/ || exit 1
echo "Pre-commit checks passed."
HOOK
chmod +x .git/hooks/pre-commit

# Create a feature branch for database work
git checkout -b feature/add-database

# Tag the initial release
git checkout main
git tag -a v0.1.0 -m "Initial release — API with monitoring"
```

**Checkpoint:**
```bash
git log --oneline | head -5
git tag -l
git diff --check           # No whitespace errors
test -x .git/hooks/pre-commit && echo "✓ Pre-commit hook installed"
```

### Step 8: Add Database Integration (Section 04)

```python
# src/appcore/db/__init__.py
```

```python
# src/appcore/db/database.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path("data/predictions.db")


def init_db():
    """Initialize the database with required tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id TEXT PRIMARY KEY,
                features TEXT NOT NULL,
                result REAL NOT NULL,
                model_version TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_predictions_created_at 
            ON predictions(created_at)
        """)


@contextmanager
def get_connection():
    """Get a database connection with auto-commit/rollback."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

```python
# src/appcore/db/repository.py
import json
from appcore.db.database import get_connection


def save_prediction(prediction_id: str, features: list[float], 
                    result: float, model_version: str, created_at: str):
    """Save a prediction to the database."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO predictions (id, features, result, model_version, created_at) VALUES (?, ?, ?, ?, ?)",
            (prediction_id, json.dumps(features), result, model_version, created_at),
        )


def get_prediction(prediction_id: str) -> dict | None:
    """Retrieve a prediction by ID."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM predictions WHERE id = ?", (prediction_id,)
        ).fetchone()
        if row:
            return dict(row)
    return None


def get_recent_predictions(limit: int = 10) -> list[dict]:
    """Get the most recent predictions."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM predictions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
```

Now update the routes to save predictions and add a history endpoint:

```python
# Update src/appcore/api/routes.py — add these endpoints:

@router.get("/predictions/{prediction_id}")
def get_prediction_by_id(prediction_id: str):
    """Retrieve a stored prediction by its ID."""
    pred = repository.get_prediction(prediction_id)
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return pred


@router.get("/predictions")
def list_predictions(limit: int = 10):
    """List recent predictions."""
    return repository.get_recent_predictions(limit=limit)
```

Update `src/appcore/api/app.py` startup to initialize the database:

```python
from appcore.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Create tables on startup
    yield
```

**Optional — Add Redis caching** (requires `uv add redis`):

```python
# src/appcore/db/cache.py
import json
import redis

_client = None

def get_redis() -> redis.Redis | None:
    """Get Redis client, return None if unavailable."""
    global _client
    if _client is None:
        try:
            _client = redis.Redis(host="localhost", port=6379, decode_responses=True)
            _client.ping()
        except (redis.ConnectionError, redis.TimeoutError):
            _client = None
    return _client


def cache_prediction(prediction_id: str, data: dict, ttl: int = 3600):
    """Cache a prediction result."""
    r = get_redis()
    if r:
        r.setex(f"pred:{prediction_id}", ttl, json.dumps(data))


def get_cached_prediction(prediction_id: str) -> dict | None:
    """Get a cached prediction."""
    r = get_redis()
    if r:
        cached = r.get(f"pred:{prediction_id}")
        if cached:
            return json.loads(cached)
    return None
```

**Checkpoint:**
```bash
# Verify database works
uv run python -c "
from appcore.db.database import init_db, get_connection
init_db()
with get_connection() as conn:
    count = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    print(f'✓ Database initialized, {count} predictions stored')
"

# Verify new endpoints
uv run uvicorn appcore.api.app:app --port 8000 &
sleep 2
# Create a prediction
PRED_ID=$(curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}' | python3 -c "import sys,json; print(json.load(sys.stdin)['prediction_id'])")
echo "Created prediction: $PRED_ID"

# Retrieve it
curl -s "http://localhost:8000/predictions/$PRED_ID" | python3 -m json.tool

# List recent
curl -s http://localhost:8000/predictions | python3 -m json.tool
kill %1
```

Git commit:
```bash
git checkout feature/add-database
git add -A
git commit -m "feat: add SQLite database for prediction persistence"
git checkout main
git merge feature/add-database
git tag -a v0.2.0 -m "Add database persistence"
```

### Step 9: Add Security (Section 11)

```python
# src/appcore/api/security.py
import os
import time
import hashlib
import hmac
from functools import wraps
from datetime import datetime, timezone, timedelta

# --- API Key Authentication ---
API_KEYS = {
    os.getenv("API_KEY", "dev-key-change-in-production"): "default-user",
}

def verify_api_key(api_key: str) -> str | None:
    """Verify an API key and return the associated user, or None."""
    return API_KEYS.get(api_key)
```

```python
# src/appcore/api/auth.py
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from appcore.api.security import verify_api_key

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str = Security(api_key_header)) -> str:
    """FastAPI dependency that requires a valid API key."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include X-API-Key header.",
        )
    user = verify_api_key(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )
    return user
```

```python
# src/appcore/api/rate_limiter.py
import time
from collections import defaultdict


class InMemoryRateLimiter:
    """Simple in-memory rate limiter using sliding window."""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if the client is within rate limits."""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Remove old entries
        self._requests[client_id] = [
            t for t in self._requests[client_id] if t > window_start
        ]
        
        if len(self._requests[client_id]) >= self.max_requests:
            return False
        
        self._requests[client_id].append(now)
        return True
    
    def remaining(self, client_id: str) -> int:
        """Get remaining requests in the current window."""
        now = time.time()
        window_start = now - self.window_seconds
        recent = [t for t in self._requests[client_id] if t > window_start]
        return max(0, self.max_requests - len(recent))


rate_limiter = InMemoryRateLimiter(max_requests=100, window_seconds=60)
```

Update `app.py` to add security middleware:

```python
# Add to src/appcore/api/app.py middleware:

from appcore.api.rate_limiter import rate_limiter

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limit requests by client IP."""
    if request.url.path.startswith("/metrics"):
        return await call_next(request)
    
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."},
        )
    
    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(rate_limiter.remaining(client_ip))
    return response
```

Protect the `/predict` endpoint with API key auth:

```python
# Update src/appcore/api/routes.py:
from appcore.api.auth import require_api_key

@router.post("/predict", response_model=PredictResponse, status_code=status.HTTP_201_CREATED)
def predict(
    request: PredictRequest,
    model: PredictionModel = Depends(get_model),
    user: str = Depends(require_api_key),  # NEW: require API key
):
    # ... existing prediction logic ...
```

Create a `.env.example` file:

```bash
# .env.example — copy to .env and fill in real values
API_KEY=dev-key-change-in-production
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///data/predictions.db
REDIS_URL=redis://localhost:6379
```

**Checkpoint:**
```bash
# Test without API key (should fail)
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0]}' | python3 -m json.tool
# Expected: 401 Unauthorized

# Test with API key (should work)
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-change-in-production" \
  -d '{"features": [1.0, 2.0, 3.0]}' | python3 -m json.tool
# Expected: 201 Created

# Test rate limiting (hit 100+ requests)
for i in $(seq 1 105); do
    curl -s -o /dev/null -w "%{http_code} " http://localhost:8000/health
done
echo ""
# Should see 429 status codes toward the end
```

Git commit:
```bash
git checkout -b feature/add-security
git add -A
git commit -m "feat: add API key auth, rate limiting, and .env management"
git checkout main
git merge feature/add-security
git tag -a v0.3.0 -m "Add security features"
```

### Step 10: Add Infrastructure Configuration (Section 16)

Create a production-ready directory structure for IaC:

```bash
mkdir -p infra/terraform
mkdir -p scripts
```

```hcl
# infra/terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

variable "app_name" {
  default = "practical-production-service"
}

variable "environment" {
  default = "staging"
}

variable "app_port" {
  default = 8000
}

# Generate the Docker Compose config from Terraform
resource "local_file" "docker_compose_generated" {
  content = templatefile("${path.module}/templates/docker-compose.yml.tpl", {
    app_name    = var.app_name
    environment = var.environment
    app_port    = var.app_port
  })
  filename = "${path.module}/../../docker-compose.generated.yml"
}

# Generate environment-specific .env file
resource "local_file" "env_file" {
  content = <<-EOT
    APP_NAME=${var.app_name}
    ENVIRONMENT=${var.environment}
    APP_PORT=${var.app_port}
    LOG_LEVEL=${var.environment == "production" ? "WARNING" : "INFO"}
  EOT
  filename = "${path.module}/../../.env.${var.environment}"
}

output "compose_file" {
  value = local_file.docker_compose_generated.filename
}

output "env_file" {
  value = local_file.env_file.filename
}
```

Create a health check script for deployment:

```bash
#!/bin/bash
# scripts/health_check.sh — Verify service is running correctly
set -e

APP_URL="${1:-http://localhost:8000}"
MAX_RETRIES="${2:-10}"
RETRY_DELAY="${3:-3}"

echo "Health checking $APP_URL (max $MAX_RETRIES attempts)..."

for i in $(seq 1 "$MAX_RETRIES"); do
    if curl -sf "$APP_URL/health" > /dev/null 2>&1; then
        echo "✓ Service is healthy (attempt $i)"
        
        # Verify all key endpoints
        curl -sf "$APP_URL/version" > /dev/null && echo "  ✓ /version OK"
        curl -sf "$APP_URL/metrics" > /dev/null && echo "  ✓ /metrics OK"
        
        exit 0
    fi
    echo "  Attempt $i/$MAX_RETRIES — waiting ${RETRY_DELAY}s..."
    sleep "$RETRY_DELAY"
done

echo "✗ Service failed health check after $MAX_RETRIES attempts"
exit 1
```

```bash
chmod +x scripts/health_check.sh
```

**Checkpoint:**
```bash
# Test health check script
docker compose up -d
./scripts/health_check.sh http://localhost:8000
docker compose down
```

### Step 11: Add Nginx Reverse Proxy (Section 12)

```nginx
# configs/nginx.conf
upstream app_servers {
    server api:8000;
    # Add more servers for load balancing:
    # server api-2:8000;
    # server api-3:8000;
}

# Rate limiting zone
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/s;

server {
    listen 80;
    server_name localhost;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_types application/json text/plain text/css;
    gzip_min_length 256;

    # API proxy
    location / {
        limit_req zone=api_limit burst=20 nodelay;
        
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;

        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
        proxy_send_timeout 10s;
    }

    # Metrics endpoint — no rate limit (internal scraping)
    location /metrics {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
    }

    # Health check for the proxy itself
    location /nginx-health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
```

Update `docker-compose.yml` to include Nginx:

```yaml
# docker-compose.yml (updated with full stack)
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./configs/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      api:
        condition: service_healthy
    restart: unless-stopped

  api:
    build: .
    expose:
      - "8000"       # Only expose internally (Nginx handles external traffic)
    environment:
      - APP_NAME=practical-production-service
      - LOG_LEVEL=INFO
      - API_KEY=dev-key-change-in-production
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

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

**Checkpoint:**
```bash
# Start the full stack with Nginx
docker compose up -d
sleep 5

# Access through Nginx (port 80) instead of direct API (port 8000)
curl -s http://localhost/health | python3 -m json.tool
curl -s http://localhost/nginx-health
curl -s -X POST http://localhost/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-change-in-production" \
  -d '{"features": [1.0, 2.0, 3.0]}' | python3 -m json.tool

# Verify security headers
curl -sI http://localhost/health | grep -i "x-frame\|x-content\|x-xss"

# Check Nginx logs
docker compose logs nginx | tail -10

docker compose down
```

Git commit:
```bash
git checkout -b feature/add-nginx
git add -A
git commit -m "feat: add Nginx reverse proxy with rate limiting and security headers"
git checkout main
git merge feature/add-nginx
git tag -a v1.0.0 -m "Production-ready release with full stack"
```

### Step 12: Verify Everything Works Together

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
echo "--- Section 05 & 06: API ---"
check "Routes module exists" "test -f src/appcore/api/routes.py"
check "Schemas module exists" "test -f src/appcore/api/schemas.py"
check "App module exists" "test -f src/appcore/api/app.py"

echo ""
echo "--- Section 06: Testing ---"
check "Test files exist" "ls tests/test_*.py"
check "Tests pass" "uv run pytest tests/ -q"
check "Linting passes" "uv run ruff check src/ tests/"

echo ""
echo "--- Section 09: Docker ---"
check "Dockerfile exists" "test -f Dockerfile"
check ".dockerignore exists" "test -f .dockerignore"
check "docker-compose.yml exists" "test -f docker-compose.yml"
check "Image builds" "docker build -t capstone-verify:test . -q"

echo ""
echo "--- Section 13: CI/CD ---"
check "CI workflow exists" "test -f .github/workflows/ci.yml"

echo ""
echo "--- Section 15: Monitoring ---"
check "Metrics module exists" "test -f src/appcore/monitoring/metrics.py"
check "Prometheus config exists" "test -f configs/prometheus.yml"

echo ""
echo "--- Section 02: Git ---"
check "Git repo initialized" "test -d .git"
check "Pre-commit hook exists" "test -x .git/hooks/pre-commit"
check ".gitignore exists" "test -f .gitignore"
check "Has git tags" "git tag -l | grep -q v"

echo ""
echo "--- Section 04: Database ---"
check "Database module exists" "test -f src/appcore/db/database.py"
check "Repository module exists" "test -f src/appcore/db/repository.py"

echo ""
echo "--- Section 11: Security ---"
check "Auth module exists" "test -f src/appcore/api/auth.py"
check "Rate limiter exists" "test -f src/appcore/api/rate_limiter.py"
check ".env.example exists" "test -f .env.example"
check "No secrets in source" "! grep -r 'password\|secret\|api_key' src/ --include='*.py' -l | grep -v security.py | grep -v __pycache__"

echo ""
echo "--- Section 16: Infrastructure ---"
check "Health check script exists" "test -x scripts/health_check.sh"

echo ""
echo "--- Section 12: Nginx ---"
check "Nginx config exists" "test -f configs/nginx.conf"

echo ""
echo "--- Integration: Smoke Test ---"
docker compose up -d > /dev/null 2>&1
sleep 8

check "GET /health returns 200 (via Nginx)" "curl -sf http://localhost/health"
check "GET /version returns 200" "curl -sf http://localhost/version"
check "POST /predict returns 201" "curl -sf -o /dev/null -w '%{http_code}' -X POST http://localhost/predict -H 'Content-Type: application/json' -H 'X-API-Key: dev-key-change-in-production' -d '{\"features\": [1.0, 2.0]}' | grep 201"
check "POST /predict without API key returns 401" "curl -sf -o /dev/null -w '%{http_code}' -X POST http://localhost/predict -H 'Content-Type: application/json' -d '{\"features\": [1.0]}' | grep 401"
check "GET /metrics returns prometheus format" "curl -sf http://localhost/metrics | grep http_requests_total"
check "GET /predictions returns list" "curl -sf http://localhost/predictions"
check "Invalid request returns 422" "curl -sf -o /dev/null -w '%{http_code}' -X POST http://localhost/predict -H 'Content-Type: application/json' -H 'X-API-Key: dev-key-change-in-production' -d '{\"features\": []}' | grep 422"
check "Nginx health endpoint works" "curl -sf http://localhost/nginx-health"
check "Security headers present" "curl -sI http://localhost/health | grep -i X-Content-Type-Options"

docker compose down > /dev/null 2>&1

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

**API (Sections 5, 6):**
- `GET /health` — returns health status with dependency checks, 200 if healthy, 503 if not
- `GET /version` — returns app version, API version, model version
- `POST /predict` — accepts JSON `{"features": [float, ...]}`, returns prediction with ID, result, model version, timestamp
- `GET /predictions` — list recent predictions from the database
- `GET /predictions/{id}` — retrieve a specific prediction
- `GET /metrics` — Prometheus-compatible text format
- All responses use Pydantic models
- Request validation with meaningful error messages
- Request ID tracking via middleware
- Structured JSON logging

**Testing (Section 06):**
- Minimum 15 tests covering all endpoints (including new DB and auth endpoints)
- Test happy path AND error cases
- Test authentication and authorization
- All tests pass with `uv run pytest`

**Docker (Section 09):**
- Multi-stage Dockerfile (build + production stages)
- Non-root user in production stage
- Health check configured
- `docker-compose.yml` with API + Prometheus + Nginx + Redis
- Image size under 200MB

**CI (Section 13):**
- GitHub Actions workflow
- Lint → Test → Docker build pipeline
- Smoke test in CI

**Monitoring (Section 15):**
- Request counter with method, endpoint, status labels
- Request latency histogram
- Prediction counter and latency histogram
- Health gauge
- Prometheus scrape configuration

**Git Workflow (Section 02):**
- Proper `.gitignore` (no `.venv/`, `__pycache__/`, `.env`, `*.db`)
- Feature branches for each major addition
- Meaningful commit messages (conventional commits: `feat:`, `fix:`, `docs:`)
- Pre-commit hook running linter
- Semantic version tags (v0.1.0, v0.2.0, v1.0.0)

**Database (Section 04):**
- SQLite for prediction storage
- Database initialization on startup
- Repository pattern with `save_prediction()` and `get_prediction()`
- Context manager for connections with proper commit/rollback
- Index on frequently queried columns

**Security (Section 11):**
- API key authentication on `/predict` endpoint
- Rate limiting middleware (100 requests/minute per IP)
- `.env.example` with all required environment variables
- No hardcoded secrets in source code
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)

**Infrastructure (Section 16):**
- Health check script for deployment verification
- Environment-specific configuration support

**Nginx (Section 12):**
- Reverse proxy forwarding to API on port 80
- Rate limiting zone for API endpoints
- Security headers added at proxy level
- Gzip compression enabled
- Proper proxy headers (X-Real-IP, X-Forwarded-For)
- Separate Nginx health endpoint (`/nginx-health`)

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
- It was set up manually — no Dockerfile, no CI, no monitoring, no database
- Customers are complaining about intermittent errors and slow responses
- There's no authentication — anyone can hit the API
- Nobody knows what Python version or dependencies are installed
- The previous developer's git history is a mess (no branches, no tags)
- The team wants to move to a modern, reproducible, secure setup

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
> 5. **Store predictions.** Right now predictions are fire-and-forget. We need to store them so customers can retrieve past results. Add a database.
>
> 6. **Lock it down.** The API is currently open to anyone. Add authentication and rate limiting. We've had abuse from scrapers hitting us thousands of times a minute.
>
> 7. **Put it behind Nginx.** We need a proper reverse proxy. Handle SSL termination, add security headers, set up rate limiting at the proxy level too.
>
> 8. **Clean up the git workflow.** Use proper branching, tags, and commit messages. Set up a pre-commit hook so broken code never gets committed.
>
> 9. **Document your decisions.** Write a `DECISIONS.md` file explaining what you chose and why."
>
> No, you can't ask the previous developer. They left a month ago.

### Deliverables

1. **Complete project** with all source code in `src/appcore/`
2. **Database layer** — schema, repository, migrations
3. **Authentication** — API key auth on protected endpoints
4. **Rate limiting** — at both application and Nginx level
5. **Dockerfile** with multi-stage build
6. **docker-compose.yml** with API + Nginx + Prometheus + Redis
7. **Nginx config** with reverse proxy, security headers, compression
8. **CI/CD pipeline** (`.github/workflows/ci.yml`)
9. **Tests** with >80% endpoint coverage including auth and DB tests
10. **Git history** with feature branches, meaningful commits, and semantic tags
11. **DECISIONS.md** explaining:
   - Why you chose `uv` over pip/poetry
   - Why src-layout over flat layout
   - Your Docker strategy (base image, multi-stage rationale, image size)
   - Your monitoring approach (what metrics, why those buckets)
   - Your testing strategy (what you test and why)
   - Your database choice (SQLite vs PostgreSQL) and schema design
   - Your authentication approach and why not JWT/OAuth
   - Your Nginx configuration choices (rate limits, timeouts, headers)
   - Your Git branching strategy
12. **README.md** with setup and run instructions

### Challenges You'll Face

These are deliberately vague or ambiguous — just like real requirements:

- "Latency percentiles" — which ones? You decide (and justify in DECISIONS.md)
- "Enough tests" — what's enough? Your call
- "JSON logs so our log aggregator can parse them" — what fields? You figure it out
- "Other services depend on the API" — so you need to test the contract, not just happy path
- "Make it reproducible" — does that include the Prometheus config? The Docker compose? You decide
- "Store predictions" — what schema? Do you need migrations? What about cleanup of old data?
- "Add authentication" — API keys? JWT? OAuth? What's appropriate for an internal ML service?
- "Rate limiting" — how many requests per minute? Per user? Per IP? At which layer?
- "Put it behind Nginx" — do you need SSL? What about WebSocket support? How do you handle timeouts?
- "Clean up the git workflow" — what branching strategy? Git flow? GitHub flow? Trunk-based?

### How to Evaluate Level 3

**Functional requirements** (must work):
- `docker compose up` starts API + Nginx + Prometheus + Redis
- `curl http://localhost/health` returns 200 (through Nginx on port 80)
- `curl /predict` with valid features and API key returns 201 with correct schema
- `curl /predict` without API key returns 401
- `curl /predictions` returns stored prediction history
- `curl /metrics` returns Prometheus text format
- `curl /nginx-health` returns 200
- `uv run pytest` — all tests pass
- `uv run ruff check` — no errors
- CI workflow syntax is valid
- Git has at least 3 feature branches and semantic version tags

**Non-functional requirements** (must be reasonable):
- Docker image under 200MB
- p95 latency under 100ms for `/health`
- p95 latency under 500ms for `/predict`
- Zero test flakiness (run `pytest` 3 times, all pass)
- No secrets hardcoded in source (use env vars)
- Security headers present in all responses (via Nginx)

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

### Database (Section 04)
- [ ] `src/appcore/db/database.py` — connection management, init_db()
- [ ] `src/appcore/db/repository.py` — save/get/list predictions
- [ ] `GET /predictions` endpoint returns stored predictions
- [ ] `GET /predictions/{id}` endpoint retrieves by ID
- [ ] Database initializes on app startup

### Security (Section 11)
- [ ] `src/appcore/api/auth.py` — API key authentication dependency
- [ ] `src/appcore/api/security.py` — key verification logic
- [ ] `src/appcore/api/rate_limiter.py` — rate limiting implementation
- [ ] `.env.example` — document all required environment variables
- [ ] `/predict` requires valid API key header
- [ ] Rate limiting returns 429 when exceeded

### Container & Deployment
- [ ] `Dockerfile` — multi-stage, non-root, health check
- [ ] `.dockerignore` — excludes unnecessary files
- [ ] `docker-compose.yml` — API + Nginx + Prometheus + Redis
- [ ] `configs/prometheus.yml` — scrape configuration
- [ ] `configs/nginx.conf` — reverse proxy with security headers

### Infrastructure (Section 16)
- [ ] `scripts/health_check.sh` — deployment verification script

### Nginx (Section 12)
- [ ] Nginx reverse proxy on port 80
- [ ] Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- [ ] Rate limiting zone configured
- [ ] Gzip compression enabled
- [ ] `/nginx-health` endpoint for proxy health checks

### Testing & CI
- [ ] `tests/conftest.py` — shared fixtures
- [ ] `tests/test_health.py` — health endpoint tests
- [ ] `tests/test_version.py` — version endpoint tests
- [ ] `tests/test_predict.py` — prediction tests (valid + invalid + auth)
- [ ] `tests/test_metrics.py` — monitoring tests
- [ ] `tests/test_db.py` — database CRUD tests
- [ ] `tests/test_auth.py` — authentication tests (valid key, missing key, invalid key)
- [ ] `.github/workflows/ci.yml` — CI pipeline

### Git Workflow (Section 02)
- [ ] `.gitignore` — proper exclusions
- [ ] Pre-commit hook running linter
- [ ] Feature branches for each major addition
- [ ] Meaningful commit messages with conventional format
- [ ] Semantic version tags (v0.1.0 → v1.0.0)

### Endpoints
- [ ] `GET /health` → 200 with status, checks, timestamp
- [ ] `GET /version` → 200 with version, api_version, model_version
- [ ] `POST /predict` (with API key) → 201 with prediction_id, result, model_version, created_at
- [ ] `POST /predict` (no API key) → 401 Unauthorized
- [ ] `POST /predict` (invalid data) → 422 with error details
- [ ] `GET /predictions` → 200 with list of recent predictions
- [ ] `GET /predictions/{id}` → 200 with specific prediction or 404
- [ ] `GET /metrics` → Prometheus text format with all custom metrics
- [ ] `GET /nginx-health` → 200 (via Nginx)

### Quality
- [ ] All tests pass: `uv run pytest -v`
- [ ] Lint clean: `uv run ruff check src/ tests/`
- [ ] Docker image builds successfully
- [ ] Docker compose brings up full stack (API + Nginx + Prometheus + Redis)
- [ ] Prometheus can scrape the API metrics
- [ ] Nginx proxies requests correctly
- [ ] Security headers present in responses
- [ ] Rate limiting works at both application and Nginx level

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
| 8 | Git workflow | Branching, tags, hooks, meaningful commit history |
| 9 | Database | SQLite persistence, repository pattern, context managers |
| 10 | Security | API key auth, rate limiting, secrets management, headers |
| 11 | Infrastructure | Health check scripts, environment configuration, IaC |
| 12 | Nginx | Reverse proxy, load balancing, security headers, compression |

**You can now:**
- Set up a Python project from scratch with reproducible dependencies
- Build a production-quality REST API with authentication and persistence
- Containerize and deploy it behind Nginx
- Secure it with auth, rate limiting, and security headers
- Store data in a database with proper connection management
- Monitor it with metrics and structured logs
- Automate testing and deployment with CI/CD
- Manage code with professional Git workflows

**This is exactly what production engineering teams do every day.**

---

*Previous: [Section 19 — RDF & SPARQL Labs](19-rdf-sparql-labs.md)*

*Congratulations on completing the core curriculum! You have completed the entire Production Engineering Bootcamp!*
