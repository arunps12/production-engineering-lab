# SECTION 15 — MONITORING THEORY & PRACTICE

---

## PART A — CONCEPT EXPLANATION

### What is Observability?

**Observability** is the ability to understand what's happening inside your system by examining its outputs. A system is observable if you can answer: "Why is it broken?" without deploying new code or guessing.

The **three pillars of observability:**

```
                    Observability
                    /     |     \
               Metrics   Logs   Traces
               (what)   (why)  (where)
```

- **Metrics** — numerical measurements over time: request count, latency, CPU usage
- **Logs** — timestamped textual records of events: "User 42 logged in", "Database query failed"
- **Traces** — end-to-end journey of a request across services: frontend → API → database → response

**Why observability matters:** In production, you can't attach a debugger. You can't `print()`. You can't reproduce the exact conditions. Your **only** information comes from what the system reports about itself.

### Metrics vs Logs vs Traces

| Aspect | Metrics | Logs | Traces |
|---|---|---|---|
| Format | Numbers | Text | Structured spans |
| Volume | Low (aggregated) | High | Medium |
| Cost | Cheap to store | Expensive at scale | Medium |
| Use case | Alerting, dashboards | Debugging specific events | Cross-service debugging |
| Example | "500 errors in last minute: 23" | "Error: DB connection refused at 10:03:21" | "Request abc123: API→DB→response took 450ms" |
| Tool | Prometheus, Datadog | ELK, Loki | Jaeger, Zipkin |

**Mental model:**
- **Metrics** are like a car's dashboard gauges: speed, fuel, temperature. You glance at them to see if something is wrong.
- **Logs** are like the engine's diagnostic log. When the temperature gauge spikes, you read the logs to find out WHY.
- **Traces** are like a GPS track. When a delivery is late, you see exactly where in the route it got stuck.

### What is Latency?

**Latency** = the time it takes to handle a request. It's the single most important metric for user experience.

```
Client sends request → [LATENCY] → Client receives response
```

**Why averages lie:**
```
Requests: 99 × 10ms + 1 × 10000ms = 10,990ms total
Average:  10,990 / 100 = 109.9ms  ← Looks OK!
p99:      10,000ms                 ← 1% of users wait 10 seconds!
```

**Use percentiles:**
- **p50** (median) — half of requests are faster than this
- **p95** — 95% of requests are faster (important for SLAs)
- **p99** — 99% of requests are faster (catches tail latency)
- **p99.9** — for critical services (payment processing, etc.)

### What is a Histogram?

A **histogram** groups observations into buckets:

```
Response time histogram (ms):
  ≤10ms:    ████████████████████  (200 requests)
  ≤25ms:    ██████████            (100 requests)
  ≤50ms:    ████                  (40 requests)
  ≤100ms:   ██                    (20 requests)
  ≤250ms:   █                     (10 requests)
  ≤500ms:                         (2 requests)
  ≤1000ms:  ▏                     (1 request)
  >1000ms:                        (0 requests)
```

**Why histograms over averages:** Histograms give you the **distribution**. You can calculate any percentile from a histogram. From an average, you can't see the distribution.

**Prometheus histogram** records:
- `_bucket` — count of observations per bucket
- `_sum` — total sum of observed values
- `_count` — total number of observations

From these, you can compute p50, p95, p99 at query time.

### What is Error Rate?

**Error rate** = percentage of requests that result in errors (usually 5xx status codes).

```
Error rate = (errors / total_requests) × 100

Example:
  Total requests in last minute: 1000
  5xx responses: 15
  Error rate: 1.5%
```

**Common SLA targets:**
- 99.9% availability → max 0.1% error rate → ~43 minutes of errors per month
- 99.99% availability → max 0.01% error rate → ~4 minutes per month

**What to track:**
- Overall error rate
- Error rate per endpoint (`/predict` might be 5% while `/health` is 0%)
- Error rate by type (400s = client errors, 500s = server bugs)

### Why Monitoring Matters in Production

**Without monitoring:**
```
User: "The app is slow"
You:  "Works fine for me" (tests passing, can't see real traffic)
User: "It's been slow for 3 hours"
You:  "Let me SSH in and check..." (reactive, slow)
```

**With monitoring:**
```
Alert at 10:03: "p99 latency > 500ms on /predict endpoint"
Dashboard shows: latency spike correlates with memory increase
Logs show: "GC pause: 2.3 seconds" at 10:02
Root cause: model loaded twice into memory → GC pressure
Fix: restart service, add memory limit → resolved in 5 minutes
```

**The four golden signals** (from Google's SRE book):
1. **Latency** — how long requests take
2. **Traffic** — how many requests per second
3. **Errors** — how many requests fail
4. **Saturation** — how full your resources are (CPU, memory, disk)

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "Logging is enough" | Logs can't tell you "error rate increased 50% in the last minute" — metrics can |
| "I'll add monitoring later" | Instrumenting after a production issue means you're blind during the most critical moments |
| "More metrics = better" | Too many metrics create noise. Focus on the four golden signals first |
| "Average latency is fine" | Averages hide tail latency. Use p95/p99 |
| "Health check = monitoring" | Health check tells you alive/dead. Monitoring tells you fast/slow, accurate/broken |
| "Prometheus is hard" | The client library is ~10 lines of code. The hardest part is deciding what to measure |

---

## PART B — BEGINNER PRACTICE

### Exercise 7.B.1 — Add prometheus_client to Your Project

```bash
cd ~/Projects/practical-production-service

# prometheus_client should already be in dependencies from Section 0
# Verify:
uv run python -c "import prometheus_client; print(prometheus_client.__version__)"
```

### Exercise 7.B.2 — Create the Metrics Module

```python
# src/appcore/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Info

# Request counter: total number of requests
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"],
)

# Request latency histogram
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Error counter
ERROR_COUNT = Counter(
    "http_errors_total",
    "Total number of HTTP errors",
    ["method", "endpoint", "error_type"],
)

# Prediction-specific metrics
PREDICTION_COUNT = Counter(
    "predictions_total",
    "Total number of predictions made",
    ["model_version"],
)

PREDICTION_LATENCY = Histogram(
    "prediction_duration_seconds",
    "Time to run model prediction",
    ["model_version"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.5, 1.0],
)

# Application info
APP_INFO = Info(
    "app",
    "Application information",
)
```

### Exercise 7.B.3 — Instrument the Middleware

```python
# src/appcore/api/app.py — update middleware to record metrics
import time
import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from appcore.api.routes import router
from appcore.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY, APP_INFO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("appcore")

app = FastAPI(
    title="Practical Production Service",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Set application info metric
APP_INFO.info({
    "version": "0.1.0",
    "python_version": "3.11",
})


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    # Skip metrics endpoint to avoid recursion
    if request.url.path == "/metrics":
        return await call_next(request)
    
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    duration = time.perf_counter() - start_time
    
    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)
    
    # Log with request ID
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "%s %s → %d (%.3fs) [%s]",
        request.method,
        request.url.path,
        response.status_code,
        duration,
        request_id,
    )
    
    return response


app.include_router(router)
```

### Exercise 7.B.4 — Instrument the Prediction Endpoint

```python
# src/appcore/api/routes.py — add prediction metrics
import time
from appcore.monitoring.metrics import PREDICTION_COUNT, PREDICTION_LATENCY

@router.post("/predict", response_model=PredictResponse, status_code=status.HTTP_201_CREATED)
def predict(request: PredictRequest, model: PredictionModel = Depends(get_model)):
    # Time the prediction
    start = time.perf_counter()
    result = model.predict(request.features)
    duration = time.perf_counter() - start
    
    # Record metrics
    PREDICTION_COUNT.labels(model_version=model.version).inc()
    PREDICTION_LATENCY.labels(model_version=model.version).observe(duration)
    
    return PredictResponse(
        prediction_id=str(uuid.uuid4()),
        result=result,
        model_version=model.version,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
```

### Exercise 7.B.5 — View the Metrics Endpoint

```bash
uv run uvicorn appcore.api.app:app --reload --port 8000 &
sleep 2

# Generate some traffic
for i in $(seq 1 20); do
    curl -s http://localhost:8000/health > /dev/null
    curl -s -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"features": [1.0, 2.0, 3.0]}' > /dev/null
done

# Generate some errors
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": []}' > /dev/null

curl -s http://localhost:8000/nonexistent > /dev/null

# View the metrics
curl -s http://localhost:8000/metrics
```

**Expected output (excerpt):**
```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/health",method="GET",status_code="200"} 20.0
http_requests_total{endpoint="/predict",method="POST",status_code="201"} 20.0
http_requests_total{endpoint="/predict",method="POST",status_code="422"} 1.0

# HELP http_request_duration_seconds HTTP request duration in seconds
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{endpoint="/health",method="GET",le="0.005"} 18.0
http_request_duration_seconds_bucket{endpoint="/health",method="GET",le="0.01"} 20.0

# HELP predictions_total Total number of predictions made
# TYPE predictions_total counter
predictions_total{model_version="v1.0"} 20.0
```

```bash
kill %1
```

### Exercise 7.B.6 — Understand Prometheus Metric Types

```python
# COUNTER: only goes up (resets to 0 on process restart)
# Use for: total requests, total errors, total bytes transferred
from prometheus_client import Counter
requests = Counter("requests_total", "Total requests")
requests.inc()      # +1
requests.inc(5)     # +5
# requests.dec()    # ERROR — counters can't go down

# GAUGE: goes up and down
# Use for: current connections, queue size, temperature
from prometheus_client import Gauge
active_connections = Gauge("active_connections", "Current active connections")
active_connections.inc()    # +1
active_connections.dec()    # -1
active_connections.set(42)  # set to exact value

# HISTOGRAM: records distributions
# Use for: request duration, response size
from prometheus_client import Histogram
latency = Histogram("request_seconds", "Request latency", buckets=[0.01, 0.1, 1.0])
latency.observe(0.05)  # Record an observation

# SUMMARY: similar to histogram but with pre-calculated quantiles
# Use sparingly — histograms are generally preferred
from prometheus_client import Summary
duration = Summary("request_duration", "Request duration")
duration.observe(0.05)
```

### Exercise 7.B.7 — Write Tests for Metrics

```python
# tests/test_metrics.py
from fastapi.testclient import TestClient
from appcore.api.app import app

client = TestClient(app)


def test_metrics_endpoint_exists():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


def test_metrics_increment_on_request():
    # Make a health request
    client.get("/health")
    
    # Check metrics
    response = client.get("/metrics")
    assert "http_requests_total" in response.text
    assert 'endpoint="/health"' in response.text


def test_prediction_metrics():
    client.post("/predict", json={"features": [1.0, 2.0, 3.0]})
    
    response = client.get("/metrics")
    assert "predictions_total" in response.text
    assert "prediction_duration_seconds" in response.text
```

```bash
uv run pytest tests/test_metrics.py -v
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 7.C.1 — Structured JSON Logging

```python
# src/appcore/api/app.py — replace basic logging with structured JSON
import json
import logging
import sys


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields if present
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "path"):
            log_data["path"] = record.path
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(getattr(logging, level.upper()))
    
    return logging.getLogger("appcore")
```

**Why structured logging?** Plain text logs are hard to search and aggregate. JSON logs can be parsed by log aggregation tools (ELK, Loki, CloudWatch) and searched with structured queries.

### Exercise 7.C.2 — Add Health Check with Dependency Status

```python
# src/appcore/api/routes.py — enhanced health check
from prometheus_client import Gauge

HEALTH_STATUS = Gauge(
    "app_health_status",
    "Application health status (1=healthy, 0=unhealthy)",
)


@router.get("/health")
def health_check(model: PredictionModel = Depends(get_model)):
    checks = {
        "model_loaded": model.is_healthy(),
        "uptime_seconds": round(time.time() - _start_time, 2),
    }
    
    all_healthy = all([
        checks["model_loaded"],
    ])
    
    HEALTH_STATUS.set(1 if all_healthy else 0)
    
    status_code = 200 if all_healthy else 503
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }
```

### Exercise 7.C.3 — Custom Business Metrics

```python
# src/appcore/monitoring/metrics.py — add business-relevant metrics

# Feature value distribution (helps detect data drift)
FEATURE_VALUE = Histogram(
    "prediction_feature_value",
    "Distribution of individual feature values",
    ["feature_index"],
    buckets=[0.0, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0],
)

# Prediction result distribution
PREDICTION_RESULT = Histogram(
    "prediction_result_value",
    "Distribution of prediction results",
    buckets=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)

# Active model version
MODEL_INFO = Info(
    "model",
    "Current model information",
)
```

```python
# In the predict handler, record feature metrics:
for i, feature in enumerate(request.features):
    FEATURE_VALUE.labels(feature_index=str(i)).observe(feature)

PREDICTION_RESULT.observe(result)
```

### Exercise 7.C.4 — Docker Compose with Prometheus

```yaml
# docker-compose.monitoring.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_NAME=production-service
      - LOG_LEVEL=INFO

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./configs/prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - api
```

```yaml
# configs/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "production-service"
    static_configs:
      - targets: ["api:8000"]
    metrics_path: "/metrics"
    scrape_interval: 5s
```

```bash
# Start the monitoring stack
docker compose -f docker-compose.monitoring.yml up -d

# Generate traffic
for i in $(seq 1 100); do
    curl -s http://localhost:8000/predict \
      -X POST -H "Content-Type: application/json" \
      -d '{"features": ['"$((RANDOM % 10))"'.0, '"$((RANDOM % 10))"'.0]}' > /dev/null
done

# Open Prometheus UI
echo "Prometheus: http://localhost:9090"

# Example PromQL queries:
# rate(http_requests_total[5m])                    — requests per second
# histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))  — p95 latency
# sum(rate(http_errors_total[5m]))                 — error rate
# predictions_total                                — total predictions

# Stop
docker compose -f docker-compose.monitoring.yml down
```

### Exercise 7.C.5 — Error Rate Alerting Logic

```python
# Alerting rules (for Prometheus Alertmanager)
# This would go in a prometheus rules file, but understanding the logic is key

# Calculate error rate:
# rate(http_requests_total{status_code=~"5.."}[5m]) 
# /
# rate(http_requests_total[5m]) 
# > 0.05
# → Alert if error rate exceeds 5%

# Calculate p99 latency:
# histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
# > 1.0
# → Alert if p99 latency exceeds 1 second
```

Simulated alerting in Python:

```python
# src/appcore/monitoring/alerting.py
from appcore.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY
import logging

logger = logging.getLogger("appcore.alerting")

def check_error_rate(threshold: float = 0.05):
    """Log warning if error rate exceeds threshold."""
    total = 0
    errors = 0
    
    # Sum across all labels
    for metric in REQUEST_COUNT.collect():
        for sample in metric.samples:
            if sample.name == "http_requests_total":
                status = sample.labels.get("status_code", "")
                total += sample.value
                if status.startswith("5"):
                    errors += sample.value
    
    if total > 0:
        error_rate = errors / total
        if error_rate > threshold:
            logger.warning(
                "HIGH ERROR RATE: %.2f%% (threshold: %.2f%%)",
                error_rate * 100,
                threshold * 100,
            )
```

### Exercise 7.C.6 — Log Aggregation Patterns

```bash
# Parse JSON logs with jq
docker logs production-service 2>&1 | head -10

# If logs are JSON formatted:
# Count requests per endpoint
docker logs production-service 2>&1 | \
  jq -r 'select(.path != null) | .path' | \
  sort | uniq -c | sort -rn

# Find all errors
docker logs production-service 2>&1 | \
  jq 'select(.level == "ERROR")'

# Find slow requests (>100ms)
docker logs production-service 2>&1 | \
  jq 'select(.duration_ms > 100)'

# Count errors per minute
docker logs production-service 2>&1 | \
  jq -r 'select(.level == "ERROR") | .timestamp' | \
  cut -d: -f1,2 | sort | uniq -c
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 7.D.1 — Debug: Latency Spike Detection

**Scenario:** p95 latency suddenly jumps from 50ms to 2 seconds.

```bash
# Simulate normal and degraded performance
cat > /tmp/latency_test.py <<'EOF'
import time
import random
import requests

base_url = "http://localhost:8000"

# Generate normal traffic
print("=== Normal traffic ===")
for i in range(20):
    start = time.time()
    r = requests.post(f"{base_url}/predict", 
                      json={"features": [random.random() for _ in range(3)]})
    elapsed = (time.time() - start) * 1000
    print(f"Request {i+1}: {r.status_code} in {elapsed:.1f}ms")

# Check metrics for latency distribution
print("\n=== Latency metrics ===")
r = requests.get(f"{base_url}/metrics")
for line in r.text.split("\n"):
    if "request_duration_seconds" in line and "bucket" in line and "predict" in line:
        print(line)
EOF

# Run with the server running:
# uv run python /tmp/latency_test.py
```

**Diagnostic checklist:**
```
1. Check p95 vs p50: Large gap = tail latency problem
2. Check process CPU: Is the event loop blocked?
3. Check memory: Is Python garbage collecting?
4. Check if it's endpoint-specific: Only /predict or all endpoints?
5. Check concurrent requests: Are requests queuing up?
```

### Exercise 7.D.2 — Debug: Metrics Not Updating

**Scenario:** Prometheus shows stale metrics. Counter stopped incrementing.

```bash
# Check if the metrics endpoint is working
curl -s http://localhost:8000/metrics | head -20

# Is the process the same one? (PID changed = metrics reset)
curl -s http://localhost:8000/metrics | grep process_start_time

# Common causes:
# 1. Multiple workers: each worker has its own counter
#    Fix: Use prometheus_client multiprocess mode
# 2. Server restarted: counters reset to 0
#    Fix: Prometheus handles resets automatically with rate()
# 3. Metrics endpoint mounted wrong: /metrics returns HTML
#    Fix: Check app.mount("/metrics", metrics_app) is correct
# 4. Middleware skips /metrics: metrics_middleware doesn't record its own requests
#    Fix: Correct — you should skip /metrics in the middleware
```

### Exercise 7.D.3 — Debug: Disk Full from Logs

**Scenario:** Production server disk is 95% full. Application is slow.

```bash
# Find large files
du -sh /var/log/* 2>/dev/null | sort -rh | head -10

# Find your app's logs
find / -name "*.log" -size +100M 2>/dev/null

# Check log rotation
ls -la /etc/logrotate.d/ 2>/dev/null

# Quick fix: truncate (don't delete — process has file open)
# > /var/log/app/app.log   ← truncates to 0 bytes without closing

# Proper fix: configure log rotation
cat > /tmp/logrotate.conf <<'EOF'
/var/log/app/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF

# Or use Docker's built-in log rotation:
# docker run --log-opt max-size=10m --log-opt max-file=3 myapp
```

### Exercise 7.D.4 — Debug: Memory Leak Detection

```python
# src/appcore/monitoring/metrics.py — add process metrics
from prometheus_client import Gauge
import os
import psutil  # add to dependencies: uv add psutil

PROCESS_MEMORY = Gauge(
    "process_memory_bytes",
    "Process memory usage in bytes",
    ["type"],
)

def update_process_metrics():
    """Call periodically to update process metrics."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    PROCESS_MEMORY.labels(type="rss").set(mem_info.rss)
    PROCESS_MEMORY.labels(type="vms").set(mem_info.vms)
```

```bash
# Monitor memory over time (in Prometheus):
# process_memory_bytes{type="rss"}
# If this monotonically increases → memory leak

# Quick check from terminal:
watch -n 5 'ps -p $(pgrep -f uvicorn) -o pid,rss,vsz --no-headers'
```

### Exercise 7.D.5 — Debug: Prometheus Can't Scrape Metrics

**Scenario:** Prometheus shows "target is down" for your service.

```bash
# Step 1: Is the service running?
curl http://localhost:8000/health

# Step 2: Is /metrics accessible?
curl http://localhost:8000/metrics | head -5

# Step 3: Can Prometheus reach the service? (Docker networking)
# If both are in Docker, they need to be on the same network
docker network ls
docker network inspect <network_name>

# Step 4: Check Prometheus targets page
# Open http://localhost:9090/targets
# It shows the status and last scrape error for each target

# Step 5: Check Prometheus config
docker exec prometheus cat /etc/prometheus/prometheus.yml

# Common fixes:
# - Use container name instead of localhost in prometheus.yml
# - Ensure both services are on the same Docker network
# - Check metrics_path is correct (/metrics, not /prometheus/metrics)
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Full Monitoring Stack for `practical-production-service`

**Task:** Implement comprehensive monitoring with metrics, structured logging, and health checks.

**Complete Monitoring Implementation:**

```python
# src/appcore/monitoring/metrics.py — FINAL VERSION
from prometheus_client import Counter, Histogram, Gauge, Info

# HTTP Metrics
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

# Prediction Metrics
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

# Health Metrics
HEALTH_STATUS = Gauge(
    "app_health_status",
    "Application health (1=healthy, 0=unhealthy)",
)

# Application Info
APP_INFO = Info("app", "Application metadata")
```

**Test the entire monitoring stack:**

```bash
# Start everything
docker compose -f docker-compose.monitoring.yml up -d

# Generate varied traffic
for i in $(seq 1 50); do
    # Successful predictions
    curl -s -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d "{\"features\": [$((RANDOM % 10)).0, $((RANDOM % 10)).0, $((RANDOM % 10)).0]}" > /dev/null
    
    # Health checks
    curl -s http://localhost:8000/health > /dev/null
    
    # Some invalid requests (for error metrics)
    curl -s -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"features": []}' > /dev/null
done

# Verify metrics
echo "=== Key Metrics ==="
curl -s http://localhost:8000/metrics | grep -E "^(http_requests|predictions|app_health)" | head -20

echo ""
echo "=== Prometheus Targets ==="
curl -s http://localhost:9090/api/v1/targets | python3 -m json.tool | head -20
```

**Useful PromQL Queries:**

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
* 100

# p50 latency
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))

# p95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# p99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Prediction throughput
rate(predictions_total[5m])

# Prediction p95 latency
histogram_quantile(0.95, rate(prediction_duration_seconds_bucket[5m]))
```

**Acceptance Criteria:**
- [ ] `/metrics` endpoint returns Prometheus text format
- [ ] Request counter increments on every request
- [ ] Request latency histogram records all requests
- [ ] Prediction counter tracks successful/failed predictions
- [ ] Prediction latency histogram records inference time
- [ ] Health check sets `app_health_status` gauge
- [ ] Application info metric shows version
- [ ] Logs are structured (JSON format)
- [ ] Each log line includes request ID, method, path, status, duration
- [ ] Prometheus can scrape the metrics endpoint
- [ ] All metrics tests pass: `uv run pytest tests/test_metrics.py -v`

---

## Key Takeaways

1. **Metrics, logs, and traces serve different purposes.** Use metrics for alerting, logs for debugging, traces for cross-service analysis.
2. **Use histograms, not averages.** Averages hide tail latency. p95/p99 shows what real users experience.
3. **The four golden signals** (latency, traffic, errors, saturation) cover 90% of monitoring needs.
4. **Instrument from day one.** Adding metrics to a running system is harder than building them in.
5. **Structured logging** (JSON) enables machine parsing and analysis at scale.
6. **Prometheus pull model** is simpler than push: your app just exposes `/metrics`, Prometheus scrapes it.

---

*Next: [Section 16 — Cloud & Infrastructure Basics](16-cloud-infrastructure-basics.md)*
