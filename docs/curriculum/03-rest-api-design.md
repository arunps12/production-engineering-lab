# SECTION 3 — REST THEORY & API DESIGN

---

## PART A — CONCEPT EXPLANATION

### What is REST?

**REST** (Representational State Transfer) is an architectural style for designing networked applications. It was defined by Roy Fielding in his 2000 PhD dissertation. REST is **not** a protocol — it's a set of **constraints** that, when followed, produce APIs that are predictable, scalable, and maintainable.

The key idea: **resources** (things) are identified by **URLs**, and you interact with them using **standard HTTP methods**.

```
Resource: A single user
URL:      /users/42
Methods:  GET (read), PUT (replace), PATCH (update), DELETE (remove)

Resource: Collection of users
URL:      /users
Methods:  GET (list all), POST (create new)
```

**REST is not:**
- CRUD with URLs (that's a simplification)
- JSON over HTTP (REST is format-agnostic)
- Every API that uses HTTP (most "REST" APIs violate REST constraints)

### What is Statelessness?

**Statelessness** means every request must contain **all the information** the server needs to process it. The server does not remember anything about previous requests.

```
STATEFUL (bad):
  Request 1: POST /login → server stores session
  Request 2: GET /profile → server uses stored session to know who you are
  
STATELESS (REST):
  Request 1: POST /auth/token → server returns JWT token
  Request 2: GET /profile  
             Authorization: Bearer <jwt-token>
             → server decodes token to know who you are
```

**Why statelessness matters:**
- **Scalability**: Any server can handle any request. No sticky sessions.
- **Resilience**: If a server crashes, no session data is lost.
- **Caching**: Stateless responses are cacheable.
- **Simplicity**: No session management, no session storage.

**Common violation:** Storing user state in server memory (e.g., `request.session`). When you scale to multiple server instances, sessions break unless you add a shared session store — which adds complexity and a single point of failure.

### Why HTTP Verbs Matter

HTTP defines verbs (methods) with **specific semantics**. Using the wrong verb causes confusion, breaks caching, and makes APIs unpredictable.

| Verb | Purpose | Idempotent? | Safe? | Has Body? |
|---|---|---|---|---|
| `GET` | Read a resource | Yes | Yes | No |
| `POST` | Create a new resource | No | No | Yes |
| `PUT` | Replace a resource entirely | Yes | No | Yes |
| `PATCH` | Partially update a resource | No* | No | Yes |
| `DELETE` | Remove a resource | Yes | No | No |

**Safe** = doesn't modify anything. `GET` should **never** change data.
**Idempotent** = calling it N times has the same effect as calling it once.

**Common violation:**
```
# WRONG: Using GET to delete
GET /users/42/delete   ← A crawler will follow this link and delete the user

# CORRECT:
DELETE /users/42       ← Crawlers don't send DELETE requests
```

### Why Status Codes Matter

HTTP status codes tell the client **exactly what happened** without parsing the response body.

**Categories:**
| Range | Category | Meaning |
|---|---|---|
| 1xx | Informational | Continue, switching protocols |
| 2xx | Success | Request worked |
| 3xx | Redirection | Look elsewhere |
| 4xx | Client Error | Your request is wrong |
| 5xx | Server Error | Our server broke |

**Essential status codes:**

| Code | Name | When to use |
|---|---|---|
| `200` | OK | Successful GET, PUT, PATCH |
| `201` | Created | Successful POST that created a resource |
| `204` | No Content | Successful DELETE (nothing to return) |
| `400` | Bad Request | Invalid JSON, missing required field |
| `401` | Unauthorized | Not authenticated (no/bad token) |
| `403` | Forbidden | Authenticated but not allowed |
| `404` | Not Found | Resource doesn't exist |
| `405` | Method Not Allowed | Correct URL, wrong verb (e.g., POST to a GET-only endpoint) |
| `409` | Conflict | Resource state conflict (e.g., duplicate email) |
| `422` | Unprocessable Entity | Valid JSON but semantically wrong (Pydantic validation) |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Unhandled exception in server |
| `502` | Bad Gateway | Proxy can't reach upstream server |
| `503` | Service Unavailable | Server is overloaded or in maintenance |

**Bad practice: returning `200` for errors:**
```json
HTTP/1.1 200 OK

{"error": true, "message": "User not found"}
```
This breaks HTTP clients, proxies, caching, and monitoring. Use `404` instead.

### What is Idempotency?

An operation is **idempotent** if performing it multiple times has the same effect as performing it once.

```
# IDEMPOTENT:
PUT /users/42 {"name": "Alice"}
PUT /users/42 {"name": "Alice"}   ← Same result, no side effects
PUT /users/42 {"name": "Alice"}   ← Still the same

DELETE /users/42                   ← User is deleted
DELETE /users/42                   ← User is already deleted (404, but same end state)

# NOT IDEMPOTENT:
POST /orders {"item": "book"}     ← Creates order #1
POST /orders {"item": "book"}     ← Creates order #2 (different!)
POST /orders {"item": "book"}     ← Creates order #3 (different!)
```

**Why idempotency matters:**
- Network failures cause retries. If a request times out, the client doesn't know if the server processed it.
- With idempotent operations, retrying is safe.
- With non-idempotent operations (POST), retrying can create duplicates.

**Solution for POST:** Use an `Idempotency-Key` header. The server stores the key and returns the same response for duplicate keys.

### What Breaks When APIs Are Badly Designed?

**1. Using verbs in URLs:**
```
# BAD:
POST /createUser
GET  /getUser/42
POST /deleteUser/42

# GOOD:
POST   /users
GET    /users/42
DELETE /users/42
```
Bad URLs create inconsistency. New developers can't predict the API structure.

**2. Returning wrong status codes:**
```
# BAD: 200 for everything
POST /users → 200 {"id": 1}     (should be 201)
GET  /users/999 → 200 {"error": "not found"}  (should be 404)

# Impact: Monitoring shows 0% error rate when reality is 30% errors
```

**3. Inconsistent response format:**
```
# Endpoint A returns:
{"data": {"id": 1, "name": "Alice"}}

# Endpoint B returns:
{"user": {"id": 2, "name": "Bob"}}

# Endpoint C returns:
[{"id": 3, "name": "Charlie"}]
```
Clients can't write generic error handling or parsing logic.

**4. No versioning:**
```
# You change the response format. All clients break simultaneously.
# Solution: /api/v1/users, /api/v2/users
```

**5. No pagination:**
```
GET /users → returns 10 million users in one response → OOM crash
```

### Mental Model: REST as a Filing Cabinet

Think of a REST API as a **filing cabinet**:

```
Cabinet = your API server
Drawers = resource collections (/users, /orders, /products)
Folders = individual resources (/users/42)
Labels = URLs

Actions:
- GET a folder   = take it out and read it (put it back)
- POST a folder  = create a new folder in the drawer
- PUT a folder   = replace the entire folder contents
- DELETE a folder = remove the folder
```

The key insight: you talk about **things** (nouns), not **actions** (verbs). URLs are nouns. HTTP methods are the verbs.

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "REST means returning JSON" | REST is format-agnostic. It could return XML, HTML, or binary |
| "PUT and PATCH are the same" | PUT replaces the entire resource. PATCH only updates specified fields |
| "POST is for all writes" | POST = create. PUT = replace. PATCH = partial update |
| "404 means the server is broken" | 404 means the resource doesn't exist. That's a correct response |
| "Authentication is part of REST" | REST doesn't define auth. JWT, OAuth2, API keys are separate concerns |
| "My API is RESTful because it uses HTTP" | Most APIs only follow some REST constraints. True REST includes HATEOAS (rare) |

---

## PART B — BEGINNER PRACTICE

### Exercise 3.B.1 — Identify Bad API Design

**Read these API endpoints and identify what's wrong:**

```
POST /getUserById        ← Problem: uses verb in URL, should be GET /users/{id}
GET  /deletePost/5       ← Problem: GET should not modify data, should be DELETE /posts/5
POST /api/updateUser/3   ← Problem: verb in URL, should be PUT /users/3 or PATCH /users/3
GET  /search?type=users  ← Problem: this is OK for search, but should return same format as /users
POST /login              ← Problem: this is technically an action, /auth/token is more RESTful
```

**Refactored:**
```
GET    /users/{id}
DELETE /posts/5
PATCH  /users/3
GET    /users?q=searchterm
POST   /auth/token
```

### Exercise 3.B.2 — Design a REST API on Paper

**Task:** Design the API for a simple ML prediction service. Write the endpoints, methods, request/response bodies, and status codes.

**Your API should support:**
1. Health check
2. Server version
3. Submit a prediction request
4. List past predictions
5. Get a specific prediction by ID

**Answer:**

```
GET /health
  → 200 {"status": "healthy", "timestamp": "2026-02-17T10:00:00Z"}

GET /version
  → 200 {"version": "0.1.0", "python": "3.11.7"}

POST /predict
  Request:  {"features": [1.0, 2.0, 3.0]}
  → 201 {"prediction_id": "abc123", "result": 0.95, "model": "v1"}
  → 400 {"detail": "features must be a list of numbers"}
  → 422 {"detail": [{"loc": ["body", "features"], "msg": "field required"}]}

GET /predictions
  → 200 {"items": [...], "total": 42, "page": 1, "size": 20}

GET /predictions/{id}
  → 200 {"prediction_id": "abc123", "result": 0.95, "created_at": "..."}
  → 404 {"detail": "Prediction abc123 not found"}
```

### Exercise 3.B.3 — Map Status Codes to Scenarios

Match each scenario to the correct HTTP status code:

| Scenario | Code |
|---|---|
| User submits valid prediction request | `201 Created` |
| User asks for prediction that doesn't exist | `404 Not Found` |
| User sends malformed JSON | `400 Bad Request` |
| User sends valid JSON but missing required field | `422 Unprocessable Entity` |
| Server's ML model fails to load | `500 Internal Server Error` |
| User sends request without auth token | `401 Unauthorized` |
| User is authenticated but not allowed to delete | `403 Forbidden` |
| User sends `DELETE` to an endpoint that only supports `GET` | `405 Method Not Allowed` |
| User sends too many requests in 1 minute | `429 Too Many Requests` |
| Request succeeds but there's nothing to return | `204 No Content` |

### Exercise 3.B.4 — Write the Pydantic Models

Create the request and response models for your API:

```python
# src/appcore/api/models.py
from pydantic import BaseModel, Field
from datetime import datetime


class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: datetime


class VersionResponse(BaseModel):
    version: str
    python_version: str


class PredictRequest(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=1,
        description="List of numeric features for prediction"
    )
    model_version: str | None = Field(
        default=None,
        description="Optional model version to use"
    )


class PredictResponse(BaseModel):
    prediction_id: str
    result: float
    model_version: str
    created_at: datetime


class ErrorResponse(BaseModel):
    detail: str
```

**Test the models:**
```python
# Test in Python shell
from appcore.api.models import PredictRequest

# Valid request
req = PredictRequest(features=[1.0, 2.0, 3.0])
print(req.model_dump())

# Invalid request (triggers validation error)
try:
    bad = PredictRequest(features=[])
except Exception as e:
    print(f"Validation error: {e}")
```

### Exercise 3.B.5 — Understand Response Consistency

**Design a consistent error response format:**

```python
# Every endpoint should return errors in this format:
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "Prediction with ID abc123 was not found",
        "details": null
    }
}

# Success responses can vary by endpoint but should follow:
{
    "data": { ... },             # For single resources
    "items": [ ... ],            # For collections
    "meta": {                    # For pagination
        "total": 100,
        "page": 1,
        "size": 20
    }
}
```

### Exercise 3.B.6 — URL Design Principles

```
# PRINCIPLE 1: Use nouns, not verbs
✗ /getUsers  ✗ /createUser  ✗ /deleteUser
✓ /users     ✓ /users       ✓ /users/{id}

# PRINCIPLE 2: Use plural nouns
✗ /user/42   ✗ /order/1
✓ /users/42  ✓ /orders/1

# PRINCIPLE 3: Use kebab-case (not camelCase or snake_case)
✗ /userProfiles  ✗ /user_profiles
✓ /user-profiles

# PRINCIPLE 4: Nest for relationships (max 2 levels)
✓ /users/42/orders              (user's orders)
✓ /users/42/orders/7            (specific order of a user)
✗ /users/42/orders/7/items/3    (too deep — flatten)
✓ /order-items/3                (flat alternative)

# PRINCIPLE 5: Use query parameters for filtering
✓ /users?role=admin&active=true
✓ /orders?status=pending&sort=created_at
✗ /users/admin/active/true      (not a resource hierarchy)
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 3.C.1 — Refactor a Broken API

**Here's a badly designed API. Refactor it:**

```python
# BROKEN API — find ALL the problems

from fastapi import FastAPI
app = FastAPI()

@app.get("/api/getAllUsers")                 # Problem 1: verb in URL
def get_all_users():
    return {"status": "success", "data": []} # Problem 2: unnecessary wrapper

@app.post("/api/createUser")                 # Problem 3: verb in URL
def create_user(name: str):
    return {"success": True, "id": 1}        # Problem 4: should return 201, not 200

@app.post("/api/deleteUser")                 # Problem 5: POST for delete, verb in URL
def delete_user(id: int):                    # Problem 6: id should be path param
    return {"deleted": True}                 # Problem 7: should return 204

@app.get("/api/getUser")                     # Problem 8: id in query instead of path
def get_user(id: int):
    return {"id": id, "name": "Unknown"}     # Problem 9: no 404 if not found
```

**REFACTORED:**

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

# In-memory store for demonstration
users_db: dict[int, dict] = {}
next_id = 1

@app.get("/api/v1/users", response_model=list[UserResponse])
def list_users():
    return list(users_db.values())

@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global next_id
    new_user = {"id": next_id, "name": user.name}
    users_db[next_id] = new_user
    next_id += 1
    return new_user

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return users_db[user_id]

@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    del users_db[user_id]
```

### Exercise 3.C.2 — Idempotency Testing

```bash
# Start the refactored API (save as /tmp/api_test.py first)
# uv run uvicorn api_test:app --port 8100 &

# Test idempotency of DELETE
# First delete: succeeds
# curl -X DELETE http://localhost:8100/api/v1/users/1
# Expected: 204

# Second delete: resource is already gone
# curl -X DELETE http://localhost:8100/api/v1/users/1
# Expected: 404 (same end state — user doesn't exist)

# Test idempotency of PUT (if implemented)
# curl -X PUT http://localhost:8100/api/v1/users/1 -H "Content-Type: application/json" -d '{"name": "Alice"}'
# Call it 10 times — same result every time
```

### Exercise 3.C.3 — Pagination Design

```python
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    size: int
    pages: int  # total number of pages

# Usage in endpoint:
@app.get("/api/v1/predictions")
def list_predictions(page: int = 1, size: int = 20):
    # Calculate offset
    offset = (page - 1) * size
    
    # Query database
    total = len(all_predictions)
    items = all_predictions[offset:offset + size]
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

# Client usage:
# GET /api/v1/predictions?page=1&size=20  → first 20
# GET /api/v1/predictions?page=2&size=20  → next 20
```

### Exercise 3.C.4 — Error Handling Strategy

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        }
    )

# Usage:
@app.get("/api/v1/predictions/{prediction_id}")
def get_prediction(prediction_id: str):
    prediction = db.get(prediction_id)
    if not prediction:
        raise AppError(
            code="PREDICTION_NOT_FOUND",
            message=f"No prediction with ID {prediction_id}",
            status_code=404
        )
    return prediction
```

### Exercise 3.C.5 — API Versioning Strategies

```python
# Strategy 1: URL path versioning (most common)
@app.get("/api/v1/users")
def list_users_v1():
    return [{"id": 1, "name": "Alice"}]

@app.get("/api/v2/users")
def list_users_v2():
    return [{"id": 1, "name": "Alice", "email": "alice@example.com"}]

# Strategy 2: Header versioning
@app.get("/api/users")
def list_users(request: Request):
    version = request.headers.get("API-Version", "1")
    if version == "2":
        return [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
    return [{"id": 1, "name": "Alice"}]

# Recommendation: Use URL path versioning. It's explicit, cacheable, and visible.
```

### Exercise 3.C.6 — Content Negotiation

```python
from fastapi import Request
from fastapi.responses import JSONResponse, PlainTextResponse

@app.get("/api/v1/health")
def health_check(request: Request):
    health_data = {
        "status": "healthy",
        "version": "0.1.0",
    }
    
    accept = request.headers.get("Accept", "application/json")
    
    if "text/plain" in accept:
        return PlainTextResponse(f"status={health_data['status']}")
    
    return JSONResponse(health_data)

# Test:
# curl -H "Accept: application/json" http://localhost:8000/api/v1/health
# curl -H "Accept: text/plain" http://localhost:8000/api/v1/health
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 3.D.1 — Debug: API Returns 200 for Everything

**Scenario:** A junior developer wrote an API that always returns 200. Monitoring shows 0% errors, but users are complaining about lost data.

```python
# BROKEN CODE:
@app.post("/api/v1/orders")
def create_order(data: dict):
    try:
        order = process_order(data)
        return {"status": "success", "order": order}
    except ValidationError as e:
        return {"status": "error", "message": str(e)}      # ← Returns 200!
    except DatabaseError as e:
        return {"status": "error", "message": "DB error"}  # ← Returns 200!
    except Exception as e:
        return {"status": "error", "message": "Unknown"}   # ← Returns 200!
```

**Problems:**
1. Every error returns HTTP 200 → monitoring is blind
2. Generic error messages → users can't fix their requests
3. Catching `Exception` → masks bugs

**Fix:**
```python
@app.post("/api/v1/orders", status_code=201)
def create_order(data: OrderCreate):  # Pydantic validates (422 if bad)
    try:
        order = process_order(data)
        return order
    except DatabaseError as e:
        raise HTTPException(status_code=503, detail="Database unavailable")
    # Let unexpected exceptions propagate → 500 Internal Server Error
```

### Exercise 3.D.2 — Debug: Inconsistent API Responses

**Scenario:** Three endpoints return data in different formats. The frontend team can't write generic code.

```python
# Endpoint 1:
{"result": {"user": {"id": 1, "name": "Alice"}}}

# Endpoint 2:
[{"id": 2, "name": "Bob"}]

# Endpoint 3:
{"data": {"items": [{"id": 3}], "total": 1}, "meta": {"page": 1}}
```

**Fix: Create a response envelope:**

```python
from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    data: T
    meta: dict | None = None

class ListMeta(BaseModel):
    total: int
    page: int
    size: int

# Single resource:
# {"data": {"id": 1, "name": "Alice"}, "meta": null}

# Collection:
# {"data": [{"id": 1}, {"id": 2}], "meta": {"total": 2, "page": 1, "size": 20}}
```

### Exercise 3.D.3 — Debug: N+1 Query Problem in API

**Scenario:** `GET /users` takes 10 seconds. There are only 100 users.

```python
# BROKEN: N+1 queries
@app.get("/api/v1/users")
def list_users():
    users = db.query("SELECT * FROM users")  # 1 query
    result = []
    for user in users:
        orders = db.query(f"SELECT * FROM orders WHERE user_id = {user['id']}")  # 100 queries!
        result.append({**user, "order_count": len(orders)})
    return result
# Total: 101 queries!

# FIX: Join or aggregate
@app.get("/api/v1/users")
def list_users():
    users = db.query("""
        SELECT u.*, COUNT(o.id) as order_count
        FROM users u
        LEFT JOIN orders o ON o.user_id = u.id
        GROUP BY u.id
    """)  # 1 query!
    return users
```

### Exercise 3.D.4 — Debug: Rate Limiting Not Working

**Scenario:** You've added rate limiting, but users bypass it by changing user-agents.

```python
# BROKEN: Rate limiting by user-agent (easily spoofed)
from collections import defaultdict
request_counts = defaultdict(int)

@app.middleware("http")
async def rate_limit(request, call_next):
    key = request.headers.get("User-Agent", "unknown")  # ← Easily changed!
    request_counts[key] += 1
    if request_counts[key] > 100:
        return JSONResponse({"error": "Rate limit exceeded"}, status_code=429)
    return await call_next(request)

# FIX: Rate limit by IP or authenticated user ID
@app.middleware("http")
async def rate_limit(request, call_next):
    client_ip = request.client.host  # ← Much harder to spoof
    # Or: user_id from JWT token
    request_counts[client_ip] += 1
    if request_counts[client_ip] > 100:
        return JSONResponse(
            {"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests"}},
            status_code=429,
            headers={"Retry-After": "60"}
        )
    return await call_next(request)
```

### Exercise 3.D.5 — Debug: PUT vs PATCH Confusion

**Scenario:** Users call `PUT /users/42` with a partial update and lose data.

```python
# User 42 before: {"id": 42, "name": "Alice", "email": "alice@x.com", "role": "admin"}

# Client sends PUT with partial data (intending to update just the name):
# PUT /users/42 {"name": "Alicia"}

# BROKEN PUT handler:
@app.put("/api/v1/users/{user_id}")
def update_user(user_id: int, data: dict):
    users_db[user_id] = data  # ← Replaces EVERYTHING!
    return users_db[user_id]

# Result: {"name": "Alicia"}  ← email and role are GONE!

# FIX: Separate PUT (full replace) and PATCH (partial update)
class UserUpdate(BaseModel):
    name: str
    email: str
    role: str

class UserPatch(BaseModel):
    name: str | None = None
    email: str | None = None
    role: str | None = None

@app.put("/api/v1/users/{user_id}")
def replace_user(user_id: int, data: UserUpdate):
    users_db[user_id] = data.model_dump()  # Full replacement (requires all fields)
    return users_db[user_id]

@app.patch("/api/v1/users/{user_id}")
def patch_user(user_id: int, data: UserPatch):
    current = users_db[user_id]
    update_data = data.model_dump(exclude_unset=True)  # Only fields that were sent
    current.update(update_data)
    users_db[user_id] = current
    return current
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Design the API for `practical-production-service`

**Task:** Design the complete REST API for the service described in the specification. Document every endpoint with method, URL, request body, response body, status codes, and error conditions.

**API Specification:**

```yaml
openapi: 3.0.0
info:
  title: Practical Production Service API
  version: 0.1.0

paths:
  /health:
    get:
      summary: Health check
      responses:
        200:
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: {type: string, example: "healthy"}
                  timestamp: {type: string, format: date-time}
                  uptime_seconds: {type: number}

  /version:
    get:
      summary: Service version
      responses:
        200:
          description: Current version info
          content:
            application/json:
              schema:
                type: object
                properties:
                  version: {type: string, example: "0.1.0"}
                  python_version: {type: string}
                  git_commit: {type: string, nullable: true}

  /predict:
    post:
      summary: Submit prediction
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [features]
              properties:
                features:
                  type: array
                  items: {type: number}
                  minItems: 1
      responses:
        201:
          description: Prediction created
        400:
          description: Invalid input
        422:
          description: Validation error
        500:
          description: Model inference error

  /metrics:
    get:
      summary: Prometheus metrics
      responses:
        200:
          description: Metrics in Prometheus text format
          content:
            text/plain: {}
```

**Acceptance Criteria:**
- [ ] Every endpoint uses the correct HTTP verb
- [ ] Every endpoint returns the correct status code
- [ ] Error responses follow a consistent format
- [ ] Request bodies use Pydantic models with validation
- [ ] The API is versioned (at least v1 prefix planning)
- [ ] No verbs in URLs
- [ ] POST /predict returns 201, not 200
- [ ] GET /health and GET /version are safe and idempotent
- [ ] /metrics returns Prometheus text format, not JSON

**Validation:**
```bash
# After implementing, test with:
# Correct request
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}'
# Expected: 201

# Missing features
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{}'
# Expected: 422

# Wrong method
curl -X DELETE http://localhost:8000/predict
# Expected: 405

# Non-existent endpoint
curl http://localhost:8000/nonexistent
# Expected: 404
```

---

## Key Takeaways

1. **REST is about resources (nouns), not actions (verbs).** URLs identify things; HTTP methods are the verbs.
2. **Status codes are not optional.** They drive monitoring, error handling, caching, and client behavior.
3. **Idempotency prevents data corruption** during retries. PUT and DELETE must be idempotent.
4. **Consistency is more important than cleverness.** Use the same response format everywhere.
5. **Validate input with Pydantic models**, not manual checks. Let the framework reject bad data early.
6. **Version your API from day one.** Adding /v1/ costs nothing; migrating without it costs everything.

---

*Next: [Section 4 — FastAPI Professional Practice](04-fastapi-professional.md)*
