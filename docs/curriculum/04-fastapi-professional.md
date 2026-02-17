# SECTION 4 — FASTAPI THEORY & PRACTICE

---

## PART A — CONCEPT EXPLANATION

### ASGI vs WSGI

**WSGI** (Web Server Gateway Interface) is the original Python standard for web server ↔ web application communication. it's **synchronous** — one request blocks one worker thread/process until it completes.

```
WSGI flow:
Client → nginx → gunicorn (WSGI server) → Flask/Django app
                   └── Worker 1: handling request (BLOCKED until done)
                   └── Worker 2: handling request (BLOCKED until done)
                   └── Worker 3: idle
```

**ASGI** (Asynchronous Server Gateway Interface) is the async evolution of WSGI. It supports:
- **Async/await** — a single worker can handle thousands of concurrent connections
- **WebSockets** — bidirectional communication
- **HTTP/2** — multiplexed streams
- **Server-Sent Events** — real-time push

```
ASGI flow:
Client → nginx → uvicorn (ASGI server) → FastAPI app
                   └── Event loop: handling 1000s of connections concurrently
                       ├── Request A: waiting for database (suspended, not blocking)
                       ├── Request B: computing response (running)
                       └── Request C: waiting for external API (suspended, not blocking)
```

**Mental model:** WSGI is like a restaurant with one chef per table. ASGI is like a chef who starts multiple dishes, checks on each while the others cook, and serves them as they finish.

**Why FastAPI uses ASGI:** ML inference, database queries, and external API calls involve lots of waiting. With ASGI, while one request waits for inference, hundreds more can be processed. With WSGI, each waiting request wastes an entire worker process.

### What is Uvicorn?

**Uvicorn** is an ASGI server. It does for FastAPI what Gunicorn does for Flask:

```
Your code (FastAPI app) ← defines request handlers
Uvicorn               ← manages network connections, sends requests to your app
```

Uvicorn:
1. Opens a TCP socket on the specified host:port
2. Accepts connections from clients
3. Parses HTTP requests
4. Calls your FastAPI application with the request
5. Sends the response back over the TCP connection

**You never call uvicorn functions directly.** You write FastAPI code, and uvicorn calls it.

```bash
# Development (single worker, auto-reload on code changes)
uvicorn appcore.api.app:app --reload --host 0.0.0.0 --port 8000

# Production (multiple workers via gunicorn with uvicorn workers)
gunicorn appcore.api.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Key distinction:**
- `uvicorn` = single-process ASGI server (fine for dev, decent for production)
- `gunicorn + uvicorn workers` = multi-process ASGI server (production-grade)

### What is Middleware?

**Middleware** is code that runs **before** and **after** every request. It wraps around your route handlers like layers of an onion.

```
Client request
  ↓
middleware_1 (before)    ← e.g., log request start, add request ID
  ↓
middleware_2 (before)    ← e.g., check authentication
  ↓
route_handler()          ← your actual business logic
  ↓
middleware_2 (after)     ← e.g., nothing to do
  ↓
middleware_1 (after)     ← e.g., log request duration, add headers
  ↓
Client response
```

**Common middleware uses:**
- **Request logging** — log every request's method, path, status, and duration
- **CORS** — add Cross-Origin Resource Sharing headers
- **Authentication** — validate auth tokens before reaching handlers
- **Request ID** — assign a unique ID to every request for tracing
- **Timing** — measure and report response latency

```python
from fastapi import FastAPI, Request
import time
import uuid

app = FastAPI()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time"] = f"{duration:.4f}"
    return response
```

### What is Dependency Injection?

**Dependency Injection (DI)** is a pattern where a function declares what it needs, and the framework provides it. In FastAPI, `Depends()` is the DI mechanism.

**Without DI (tightly coupled):**
```python
@app.get("/users")
def list_users():
    db = Database("postgresql://localhost/mydb")  # Hardcoded! Can't test, can't change
    return db.query("SELECT * FROM users")
```

**With DI (loosely coupled):**
```python
def get_database():
    db = Database(settings.database_url)
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Database = Depends(get_database)):
    return db.query("SELECT * FROM users")
```

**Why DI matters:**
1. **Testability** — swap the real database for a mock in tests
2. **Configurability** — change the database URL without touching route code
3. **Resource management** — `yield` ensures cleanup happens (connections closed)
4. **Reusability** — same dependency across multiple routes

**FastAPI's DI chain:**
```
get_current_user depends on get_token depends on get_request_header

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return user

# FastAPI resolves the chain:
# 1. Extract header → token
# 2. Validate token → user
# 3. Pass user to profile()
```

### How the Request Lifecycle Works

Complete lifecycle of a request in FastAPI:

```
1. CLIENT sends HTTP request to uvicorn

2. UVICORN parses the raw HTTP bytes into an ASGI event

3. MIDDLEWARE STACK (before):
   ├── Middleware 1: add request ID
   ├── Middleware 2: log request start
   └── Middleware 3: check authentication

4. ROUTING: FastAPI matches URL path + method to a handler
   /predict + POST → predict_handler()

5. DEPENDENCY RESOLUTION:
   ├── Resolve Depends(get_settings) → settings object
   ├── Resolve Depends(get_model) → ML model
   └── Inject into handler parameters

6. REQUEST VALIDATION:
   ├── Parse request body as JSON
   ├── Validate against Pydantic model (PredictRequest)
   └── If invalid → return 422 (never reaches handler)

7. HANDLER EXECUTION:
   async def predict(request: PredictRequest, model = Depends(get_model)):
       result = model.predict(request.features)
       return PredictResponse(result=result)

8. RESPONSE SERIALIZATION:
   ├── Convert PredictResponse to dict
   ├── Serialize to JSON
   └── Set Content-Type: application/json

9. MIDDLEWARE STACK (after):
   ├── Middleware 3: nothing
   ├── Middleware 2: log response status + duration
   └── Middleware 1: add X-Request-ID header

10. UVICORN sends HTTP response bytes to client
```

**Key insight:** Validation happens BEFORE your code runs. If the request body doesn't match the Pydantic model, FastAPI returns 422 automatically. You never see bad data in your handler.

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "I need to validate inputs manually" | Pydantic does it automatically. Define the model and trust it |
| "`async def` makes everything faster" | Only if you `await` I/O operations. CPU-bound work still blocks the event loop |
| "I should catch all exceptions in handlers" | Let unexpected exceptions propagate — FastAPI returns 500 and logs the traceback |
| "Middleware runs in the handler" | Middleware wraps handlers. It runs before AND after |
| "Depends() is just a function call" | It's dependency injection — FastAPI resolves, caches, and cleans up dependencies |
| "I need Flask because it's simpler" | FastAPI is equally simple for basic cases and far more capable for production |

---

## PART B — BEGINNER PRACTICE

### Exercise 4.B.1 — Create the FastAPI Application

In your `practical-production-service`, create the main application file:

```python
# src/appcore/api/app.py
from fastapi import FastAPI

app = FastAPI(
    title="Practical Production Service",
    description="A production-ready ML prediction service",
    version="0.1.0",
)
```

```bash
cd ~/Projects/practical-production-service  # or wherever you created it

# Test that it starts
uv run uvicorn appcore.api.app:app --host 0.0.0.0 --port 8000 --reload &
sleep 2

# Check it's running
curl http://localhost:8000/docs
curl http://localhost:8000/openapi.json | python3 -m json.tool | head -20

# Stop it
kill %1
```

### Exercise 4.B.2 — Add Health and Version Endpoints

```python
# src/appcore/api/routes.py
from datetime import datetime, timezone
import sys
import time

from fastapi import APIRouter

router = APIRouter()

# Track when the server started
_start_time = time.time()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": round(time.time() - _start_time, 2),
    }


@router.get("/version")
def get_version():
    return {
        "version": "0.1.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    }
```

Register the router in the app:

```python
# src/appcore/api/app.py
from fastapi import FastAPI
from appcore.api.routes import router

app = FastAPI(
    title="Practical Production Service",
    description="A production-ready ML prediction service",
    version="0.1.0",
)

app.include_router(router)
```

**Test:**
```bash
uv run uvicorn appcore.api.app:app --reload --port 8000 &
sleep 2

curl http://localhost:8000/health | python3 -m json.tool
curl http://localhost:8000/version | python3 -m json.tool

kill %1
```

### Exercise 4.B.3 — Add the Prediction Endpoint with Pydantic Models

```python
# src/appcore/api/routes.py (add to existing file)
from pydantic import BaseModel, Field
from fastapi import status
import uuid


class PredictRequest(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=1,
        description="Input features for prediction",
        examples=[[1.0, 2.0, 3.0]],
    )


class PredictResponse(BaseModel):
    prediction_id: str
    result: float
    model_version: str
    created_at: str


@router.post("/predict", response_model=PredictResponse, status_code=status.HTTP_201_CREATED)
def predict(request: PredictRequest):
    # Simple mock prediction: sum of features
    result = sum(request.features) / len(request.features)
    
    return PredictResponse(
        prediction_id=str(uuid.uuid4()),
        result=round(result, 4),
        model_version="v1.0",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
```

**Test:**
```bash
# Valid request
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}'
# Expected: 201 with prediction response

# Invalid: empty features
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": []}'
# Expected: 422 (validation error — min_length=1)

# Invalid: missing features
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{}'
# Expected: 422 (field required)

# Invalid: wrong type
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": "not a list"}'
# Expected: 422 (type error)
```

### Exercise 4.B.4 — Add Request Logging Middleware

```python
# src/appcore/api/app.py (update)
from fastapi import FastAPI, Request
from appcore.api.routes import router
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("appcore")

app = FastAPI(
    title="Practical Production Service",
    version="0.1.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    duration_ms = (time.perf_counter() - start_time) * 1000
    logger.info(
        "%s %s → %d (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    
    return response


app.include_router(router)
```

**Test:** Make several requests and watch the terminal output for log lines.

### Exercise 4.B.5 — Write Your First Test

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from appcore.api.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_predict_valid():
    response = client.post("/predict", json={"features": [1.0, 2.0, 3.0]})
    assert response.status_code == 201
    data = response.json()
    assert "prediction_id" in data
    assert "result" in data
    assert data["model_version"] == "v1.0"


def test_predict_empty_features():
    response = client.post("/predict", json={"features": []})
    assert response.status_code == 422


def test_predict_missing_body():
    response = client.post("/predict")
    assert response.status_code == 422


def test_predict_wrong_method():
    response = client.get("/predict")
    assert response.status_code == 405
```

```bash
uv run pytest tests/test_api.py -v
```

**Expected:** All 6 tests pass.

### Exercise 4.B.6 — Explore Auto-Generated Docs

```bash
uv run uvicorn appcore.api.app:app --reload --port 8000 &
sleep 2

# FastAPI auto-generates OpenAPI docs
echo "Swagger UI: http://localhost:8000/docs"
echo "ReDoc:      http://localhost:8000/redoc"
echo "OpenAPI:    http://localhost:8000/openapi.json"

# Fetch the OpenAPI spec
curl -s http://localhost:8000/openapi.json | python3 -m json.tool | head -40

kill %1
```

Open `http://localhost:8000/docs` in a browser. Notice:
- All endpoints are documented
- Request/response schemas are auto-generated from Pydantic models
- You can try requests directly from the browser

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 4.C.1 — Dependency Injection for Configuration

```python
# src/appcore/config/settings.py
from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "appcore"
    debug: bool = False
    port: int = 8000
    model_path: str = "models/default.pkl"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", "appcore"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            port=int(os.getenv("PORT", "8000")),
            model_path=os.getenv("MODEL_PATH", "models/default.pkl"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


# Singleton — created once, reused everywhere
_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings
```

```python
# src/appcore/api/routes.py (use DI)
from fastapi import Depends
from appcore.config.settings import Settings, get_settings

@router.get("/version")
def get_version(settings: Settings = Depends(get_settings)):
    return {
        "version": "0.1.0",
        "app_name": settings.app_name,
        "debug": settings.debug,
    }
```

### Exercise 4.C.2 — Dependency Injection for Business Logic

```python
# src/appcore/logic.py
import random


class PredictionModel:
    """Simulates an ML model. Replace with real model later."""
    
    def __init__(self, model_version: str = "v1.0"):
        self.model_version = model_version
        self._loaded = True
    
    def predict(self, features: list[float]) -> float:
        if not self._loaded:
            raise RuntimeError("Model not loaded")
        # Simulate prediction: weighted average + noise
        result = sum(features) / len(features) + random.gauss(0, 0.01)
        return round(result, 6)
    
    def is_healthy(self) -> bool:
        return self._loaded


# Singleton
_model: PredictionModel | None = None


def get_model() -> PredictionModel:
    global _model
    if _model is None:
        _model = PredictionModel()
    return _model
```

```python
# src/appcore/api/routes.py — update predict to use DI
from appcore.logic import PredictionModel, get_model

@router.post("/predict", response_model=PredictResponse, status_code=status.HTTP_201_CREATED)
def predict(request: PredictRequest, model: PredictionModel = Depends(get_model)):
    result = model.predict(request.features)
    
    return PredictResponse(
        prediction_id=str(uuid.uuid4()),
        result=result,
        model_version=model.model_version,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
```

### Exercise 4.C.3 — Custom Exception Handling

```python
# src/appcore/api/app.py — add exception handlers

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class PredictionError(Exception):
    def __init__(self, message: str, model_version: str | None = None):
        self.message = message
        self.model_version = model_version


@app.exception_handler(PredictionError)
async def prediction_error_handler(request: Request, exc: PredictionError):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "PREDICTION_FAILED",
                "message": exc.message,
                "model_version": exc.model_version,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )
```

### Exercise 4.C.4 — Add Request ID Middleware

```python
# src/appcore/api/app.py — add request ID middleware
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

**Test:**
```bash
# Without providing a request ID (server generates one)
curl -v http://localhost:8000/health 2>&1 | grep X-Request-ID

# With a provided request ID (server echoes it back)
curl -v -H "X-Request-ID: my-trace-123" http://localhost:8000/health 2>&1 | grep X-Request-ID
# Expected: X-Request-ID: my-trace-123
```

### Exercise 4.C.5 — Structured Logging

```python
# src/appcore/api/app.py — improve logging
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        return json.dumps(log_entry)

# Set up structured logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("appcore")
logger.handlers = [handler]
logger.setLevel(logging.INFO)
```

### Exercise 4.C.6 — Async vs Sync Handlers

```python
# SYNC handler — runs in a thread pool (fine for CPU-bound work)
@router.get("/sync-demo")
def sync_handler():
    import time
    time.sleep(1)  # Blocks the thread, but not the event loop
    return {"mode": "sync", "note": "Ran in thread pool"}


# ASYNC handler — runs on the event loop
@router.get("/async-demo")
async def async_handler():
    import asyncio
    await asyncio.sleep(1)  # Suspends, doesn't block
    return {"mode": "async", "note": "Ran on event loop"}


# BROKEN async handler — blocks the event loop!
@router.get("/broken-async")
async def broken_async_handler():
    import time
    time.sleep(1)  # BLOCKS the entire event loop! No other request can be processed!
    return {"mode": "broken", "note": "Never do this"}
```

**Rule of thumb:**
- Use `def` for CPU-bound or synchronous I/O code (FastAPI runs it in a threadpool)
- Use `async def` only if you're `await`-ing something
- NEVER use `time.sleep()` in an `async def` — use `asyncio.sleep()`

### Exercise 4.C.7 — Testing with Dependency Overrides

```python
# tests/test_api_with_mocks.py
from fastapi.testclient import TestClient
from appcore.api.app import app
from appcore.logic import PredictionModel, get_model


class MockModel(PredictionModel):
    def predict(self, features: list[float]) -> float:
        return 42.0  # Always returns 42 for predictable tests


def get_mock_model():
    return MockModel()


# Override the real model with the mock
app.dependency_overrides[get_model] = get_mock_model
client = TestClient(app)


def test_predict_with_mock():
    response = client.post("/predict", json={"features": [1.0, 2.0]})
    assert response.status_code == 201
    assert response.json()["result"] == 42.0  # Always 42!


# Clean up
def teardown_module():
    app.dependency_overrides.clear()
```

```bash
uv run pytest tests/test_api_with_mocks.py -v
```

### Exercise 4.C.8 — CORS Configuration

```python
# src/appcore/api/app.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test:
# curl -v -X OPTIONS http://localhost:8000/predict \
#   -H "Origin: http://localhost:3000" \
#   -H "Access-Control-Request-Method: POST"
# Should see Access-Control-Allow-Origin: http://localhost:3000
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 4.D.1 — Debug: `async def` Blocks the Event Loop

**Scenario:** Your FastAPI service handles 1000 req/s normally. After adding a new ML inference endpoint, it drops to 1 req/s.

```python
# BROKEN: Blocking call inside async handler
@router.post("/infer")
async def infer(request: PredictRequest):
    import time
    time.sleep(5)  # Simulates slow ML inference
    # This blocks the ENTIRE event loop for 5 seconds
    # No other request can be processed during this time
    return {"result": 0.5}
```

**Diagnosis:**
```bash
# Start the server
uv run uvicorn appcore.api.app:app --port 8000 &

# Send two concurrent requests
time curl -s http://localhost:8000/infer -X POST -H "Content-Type: application/json" -d '{"features": [1.0]}' &
time curl -s http://localhost:8000/infer -X POST -H "Content-Type: application/json" -d '{"features": [2.0]}' &
wait

# If blocking: request 2 waits for request 1 → total 10s
# If non-blocking: both run concurrently → total 5s
```

**Fix options:**

```python
# Fix 1: Use sync def (FastAPI runs it in threadpool)
@router.post("/infer")
def infer(request: PredictRequest):  # NOT async
    import time
    time.sleep(5)  # Runs in thread pool, doesn't block event loop
    return {"result": 0.5}

# Fix 2: Use run_in_executor for async context
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@router.post("/infer")
async def infer(request: PredictRequest):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, slow_ml_inference, request.features)
    return {"result": result}
```

### Exercise 4.D.2 — Debug: 422 Errors in Production

**Scenario:** Your API works in Swagger UI but clients get 422 errors.

```bash
# Client sends:
curl -X POST http://localhost:8000/predict \
  -d '{"features": [1.0, 2.0]}' 
# 422! Why?

# Missing Content-Type header! FastAPI expects application/json.
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0]}'
# 201 ✓

# Another common cause: sending form data instead of JSON
curl -X POST http://localhost:8000/predict \
  -d "features=1.0,2.0"
# 422! FastAPI expects JSON body, not form data
```

### Exercise 4.D.3 — Debug: Dependency Not Cleaning Up

**Scenario:** Database connections leak because the dependency doesn't close them.

```python
# BROKEN: No cleanup
def get_db():
    db = create_connection()
    return db  # Connection is never closed!

# FIXED: Use yield for cleanup
def get_db():
    db = create_connection()
    try:
        yield db
    finally:
        db.close()  # Always runs, even if the handler raises an exception

# EVEN BETTER: Use lifespan events for setup/teardown
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create connection pool
    app.state.db_pool = create_pool()
    yield
    # Shutdown: close connection pool
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)
```

### Exercise 4.D.4 — Debug: Middleware Order Matters

**Scenario:** Your authentication middleware runs, but the request ID isn't in the auth error response.

```python
# PROBLEM: Middleware order is REVERSED in FastAPI
# The LAST added middleware runs FIRST (outermost)

# If you add them in this order:
app.add_middleware(AuthMiddleware)      # Added second → runs FIRST (outer)
app.add_middleware(RequestIDMiddleware) # Added first → runs SECOND (inner)

# Result: Auth error is returned BEFORE RequestIDMiddleware can add the header
# The client gets no X-Request-ID on 401 responses

# FIX: Add RequestID middleware AFTER Auth (so it wraps around it)
app.add_middleware(RequestIDMiddleware) # Added second → runs FIRST
app.add_middleware(AuthMiddleware)      # Added first → runs SECOND
```

**Mental model:** Think of middleware like nesting Russian dolls. The LAST one added is the outermost doll.

### Exercise 4.D.5 — Debug: Startup Fails Silently

**Scenario:** The app starts but `/predict` always returns 500. No error in startup logs.

```python
# BROKEN: Error in dependency happens at request time, not startup
def get_model():
    model = load_model("/nonexistent/path/model.pkl")  # FileNotFoundError
    return model

# Every request to /predict triggers the error, but the app starts fine.

# FIX: Load model at startup, fail fast
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model at startup — if it fails, the server won't start
    try:
        app.state.model = load_model(settings.model_path)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise  # Server won't start
    yield

app = FastAPI(lifespan=lifespan)

def get_model():
    return app.state.model  # Already loaded, no FileNotFoundError
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Build the Complete API for `practical-production-service`

**Task:** Implement the full API following all best practices learned in this section.

**Complete File Structure:**

```python
# src/appcore/__init__.py
__version__ = "0.1.0"
```

```python
# src/appcore/config/settings.py
import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "appcore"
    version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", "appcore"),
            version=os.getenv("APP_VERSION", "0.1.0"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


_settings: Settings | None = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings
```

```python
# src/appcore/logic.py
import random
import logging

logger = logging.getLogger("appcore")


class PredictionModel:
    def __init__(self, version: str = "v1.0"):
        self.version = version
        self._loaded = True
        logger.info(f"Model {version} loaded")

    def predict(self, features: list[float]) -> float:
        if not self._loaded:
            raise RuntimeError("Model not loaded")
        result = sum(features) / len(features)
        noise = random.gauss(0, 0.01)
        return round(result + noise, 6)

    def is_healthy(self) -> bool:
        return self._loaded


_model: PredictionModel | None = None

def get_model() -> PredictionModel:
    global _model
    if _model is None:
        _model = PredictionModel()
    return _model
```

```python
# src/appcore/api/routes.py
import sys
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from appcore.config.settings import Settings, get_settings
from appcore.logic import PredictionModel, get_model

router = APIRouter()

_start_time = time.time()


class PredictRequest(BaseModel):
    features: list[float] = Field(..., min_length=1)

class PredictResponse(BaseModel):
    prediction_id: str
    result: float
    model_version: str
    created_at: str


@router.get("/health")
def health_check(model: PredictionModel = Depends(get_model)):
    return {
        "status": "healthy" if model.is_healthy() else "unhealthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": round(time.time() - _start_time, 2),
    }


@router.get("/version")
def get_version(settings: Settings = Depends(get_settings)):
    return {
        "version": settings.version,
        "app_name": settings.app_name,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    }


@router.post("/predict", response_model=PredictResponse, status_code=status.HTTP_201_CREATED)
def predict(request: PredictRequest, model: PredictionModel = Depends(get_model)):
    result = model.predict(request.features)
    return PredictResponse(
        prediction_id=str(uuid.uuid4()),
        result=result,
        model_version=model.version,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
```

```python
# src/appcore/api/app.py
import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from appcore.api.routes import router

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


# Request logging + ID middleware
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "%s %s → %d (%.1fms) [%s]",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_id,
    )
    return response


app.include_router(router)
```

```python
# src/appcore/cli.py
import uvicorn
from appcore.config.settings import get_settings


def serve():
    settings = get_settings()
    uvicorn.run(
        "appcore.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    serve()
```

**Test the full system:**

```bash
# Start via CLI entrypoint
uv run appcore-serve &
sleep 2

# Run all tests
uv run pytest tests/ -v

# Manual smoke test
curl http://localhost:8000/health | python3 -m json.tool
curl http://localhost:8000/version | python3 -m json.tool
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0, 5.0]}' | python3 -m json.tool

# Check request ID header
curl -v http://localhost:8000/health 2>&1 | grep X-Request-ID

# Stop
kill %1
```

**Acceptance Criteria:**
- [ ] `uv run appcore-serve` starts the server
- [ ] `GET /health` returns 200 with status, timestamp, uptime
- [ ] `GET /version` returns 200 with version and python version
- [ ] `POST /predict` returns 201 with prediction ID and result
- [ ] `POST /predict` with invalid body returns 422
- [ ] Every response has `X-Request-ID` header
- [ ] All requests are logged with method, path, status, and duration
- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] Server starts via CLI entrypoint (not just `uvicorn` command)

---

## Key Takeaways

1. **ASGI/uvicorn is the foundation.** Understand that uvicorn handles connections; FastAPI handles routing and validation.
2. **Pydantic validation is your first line of defense.** Bad data never reaches your business logic.
3. **Dependency injection makes code testable and configurable.** Use `Depends()` for everything external.
4. **Never block the event loop.** Use `def` (not `async def`) for synchronous/CPU operations, or use `run_in_executor`.
5. **Middleware runs on every request.** Use it for cross-cutting concerns (logging, auth, metrics).
6. **Fail fast at startup.** Load models and verify configs during startup, not during the first request.

---

*Next: [Section 5 — Docker & Containerization](05-docker-containerization.md)*
