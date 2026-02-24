# SECTION 7 — REST API CRUD LABS

---

## PART A — CONCEPT EXPLANATION

### REST and CRUD — The Foundation

Every web application is built on CRUD operations mapped to HTTP methods:

```
CRUD Operation    HTTP Method    URL Pattern          Status Code
──────────────    ───────────    ───────────          ───────────
Create            POST           /resources           201 Created
Read (list)       GET            /resources           200 OK
Read (single)     GET            /resources/{id}      200 OK
Update (full)     PUT            /resources/{id}      200 OK
Update (partial)  PATCH          /resources/{id}      200 OK
Delete            DELETE         /resources/{id}      204 No Content
```

### HTTP Methods — Semantics Matter

Each HTTP method has specific semantics:

| Method | Safe? | Idempotent? | Request Body | Response Body |
|--------|-------|-------------|-------------|---------------|
| GET | Yes | Yes | No | Yes |
| POST | No | **No** | Yes | Yes |
| PUT | No | Yes | Yes | Yes |
| PATCH | No | **Depends** | Yes | Yes |
| DELETE | No | Yes | No | No (204) |

**Safe** = No side effects (reading doesn't change state)
**Idempotent** = Multiple identical requests produce the same result

### PUT vs PATCH — The Key Distinction

This is one of the most commonly confused concepts in REST API design.

**PUT (Full Replace):**
```
PUT /users/1
{
  "username": "alice",
  "email": "alice@example.com",
  "full_name": "Alice Johnson"
}
```
- Client sends the **complete resource**
- Missing fields are treated as intentional removals
- **Always idempotent** — same PUT gives same result

**PATCH (Partial Update):**
```
PATCH /users/1
{
  "full_name": "Alice J."
}
```
- Client sends **only the fields to change**
- Omitted fields remain unchanged
- **Idempotent if** the operation is "set X to value" (not "increment X")

**SQL equivalents:**

```sql
-- PUT → UPDATE all columns
UPDATE users
SET username = 'alice',
    email = 'alice@example.com',
    full_name = 'Alice Johnson'
WHERE id = 1;

-- PATCH → UPDATE only provided columns
UPDATE users
SET full_name = 'Alice J.'
WHERE id = 1;
```

### Idempotency Deep Dive

Idempotency is critical for reliability — if a network error occurs, the client can safely retry:

```
Client                      Server
  │── POST /users ──────────→│  (creates user #42)
  │                          │
  │← 201 Created ───────────│
  │   (response lost!)      │
  │                          │
  │── POST /users ──────────→│  (creates user #43 — DUPLICATE!)
```

With PUT, retry is safe:
```
  │── PUT /users/42 ────────→│  (sets user #42 state)
  │                          │
  │← 200 OK ────────────────│
  │   (response lost!)      │
  │                          │
  │── PUT /users/42 ────────→│  (sets same state again — NO DUPLICATE)
```

### Pagination

Never return all records at once. Use pagination:

```json
GET /users?page=2&size=10

{
  "items": [...],
  "total": 47,
  "page": 2,
  "size": 10,
  "pages": 5
}
```

**Pagination strategies:**
| Strategy | Pros | Cons |
|----------|------|------|
| Offset-based (`page` + `size`) | Simple, familiar | Slow on large offsets |
| Cursor-based (`after=id`) | Fast, consistent | More complex to implement |
| Keyset (`created_at > X`) | Fast, stable | Requires sortable field |

### Error Handling

Use consistent error responses:

```json
{
  "detail": "User not found",
  "status_code": 404
}
```

**Status code guidelines:**

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Malformed JSON, missing fields |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate username/email |
| 422 | Unprocessable Entity | Valid JSON but invalid values |
| 429 | Too Many Requests | Rate limit exceeded |

### Rate Limiting

Protect your API from abuse:

```
Client A: 100 requests/minute allowed
  Request 1..100 → 200 OK
  Request 101    → 429 Too Many Requests

Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 0
  X-RateLimit-Reset: 1700000060
```

**Algorithms:**
- **Fixed window** — Count per time window (simple, but allows bursts at boundaries)
- **Sliding window** — Rolling count over the last N seconds (smoother)
- **Token bucket** — Tokens refill at fixed rate, requests consume tokens

### Input Validation with Pydantic

Pydantic v2 provides type-safe request/response models:

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=100)
```

Invalid input automatically returns 422 with detailed error messages.

### Common Beginner Misunderstandings

1. **"PUT and PATCH are the same"** — PUT replaces the entire resource. PATCH updates specific fields. Using PUT with partial data silently deletes fields.
2. **"POST is idempotent"** — No. Each POST creates a new resource. Retrying POST creates duplicates.
3. **"204 means failure"** — 204 (No Content) is a success code. It's the correct response for DELETE.
4. **"Just return 200 for everything"** — Status codes communicate semantics. Use 201 for creation, 204 for deletion, 404 for not found.
5. **"Validation in the controller is enough"** — Use Pydantic models. They validate types, constraints, and generate OpenAPI docs automatically.

---

## PART B — BEGINNER PRACTICE

### Exercise 17.B.1 — Run the CRUD App

Start the FastAPI CRUD application and explore the endpoints:

```bash
cd practice/curriculum/17-rest-api-crud-labs
uv sync
uv run uvicorn src.crud_api.main:app --reload --port 8000
```

Open http://localhost:8000/docs to see the interactive Swagger UI.

Run the smoke test:

```bash
bash scripts/curl_smoke_test.sh
```

**Practice files:**
- `practice/curriculum/17-rest-api-crud-labs/src/crud_api/main.py`
- `practice/curriculum/17-rest-api-crud-labs/src/crud_api/routes.py`

### Exercise 17.B.2 — Test CRUD Operations with curl

Create, read, update, and delete users:

```bash
# Create
curl -s -X POST http://localhost:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"username":"newuser","email":"new@test.com","full_name":"New User"}' | jq .

# Read all
curl -s http://localhost:8000/users | jq .

# Read one
curl -s http://localhost:8000/users/1 | jq .

# Update (PUT)
curl -s -X PUT http://localhost:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","email":"updated@test.com","full_name":"Alice Updated"}' | jq .

# Delete
curl -s -X DELETE http://localhost:8000/users/1 -w "\nHTTP Status: %{http_code}\n"
```

### Exercise 17.B.3 — Explore Error Responses

Trigger various error codes:

```bash
# 404 — Resource not found
curl -s http://localhost:8000/users/999 | jq .

# 422 — Validation error (invalid email)
curl -s -X POST http://localhost:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"username":"x","email":"not-an-email","full_name":""}' | jq .

# 409 — Conflict (duplicate username)
curl -s -X POST http://localhost:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","email":"dup@test.com","full_name":"Duplicate"}' | jq .
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 17.C.1 — PUT vs PATCH Deep Dive

Demonstrate the difference between PUT and PATCH:

```bash
# Check current state
curl -s http://localhost:8000/users/1 | jq .

# PATCH — only changes full_name, email stays unchanged
curl -s -X PATCH http://localhost:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"full_name": "Alice Patched"}' | jq .

# PUT — must send ALL fields, or get 422
curl -s -X PUT http://localhost:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","email":"alice@test.com","full_name":"Alice Put"}' | jq .
```

Verify PUT idempotency — run the same PUT request twice and compare responses.

### Exercise 17.C.2 — Pagination

Test pagination behavior:

```bash
# Page 1 of 2
curl -s "http://localhost:8000/users?page=1&size=3" | jq .

# Page 2 of 2
curl -s "http://localhost:8000/users?page=2&size=3" | jq .

# Beyond last page — should return empty items
curl -s "http://localhost:8000/users?page=100&size=10" | jq .
```

Study the response shape — `items`, `total`, `page`, `size`, `pages`.

### Exercise 17.C.3 — Rate Limiting

Test the sliding window rate limiter:

```bash
# Fire many requests quickly
for i in $(seq 1 60); do
  code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/users)
  echo "Request $i: $code"
done
# After exceeding the limit, you should see 429 responses
```

Examine the `X-RateLimit-*` response headers.

### Exercise 17.C.4 — Write and Run Tests

Run the pytest suite:

```bash
uv run pytest tests/ -v --tb=short
```

Study the tests:
- `test_crud.py` — 17 tests covering all endpoints, edge cases, PUT idempotency
- `test_rate_limiter.py` — 4 tests for rate limiting behavior

Add a new test: **Verify that PATCH doesn't change unspecified fields**.

**Practice files:**
- `practice/curriculum/17-rest-api-crud-labs/tests/test_crud.py`
- `practice/curriculum/17-rest-api-crud-labs/tests/test_rate_limiter.py`

---

## PART D — ADVANCED DEBUG LAB

### Exercise 17.D.1 — Debug: PUT Loses Data

**Symptom:** After a PUT request, the `full_name` field is null.

**Task:**
1. Reproduce: PUT with `username` and `email` only (no `full_name`)
2. Understand that PUT is a full replace — missing fields become null/default
3. If your schema requires `full_name`, PUT should return 422
4. Fix: Ensure all required fields are validated in the PUT schema

### Exercise 17.D.2 — Debug: Duplicate POST Creates Two Resources

**Symptom:** Client retried a POST due to network timeout and now two identical users exist.

**Task:**
1. POST is not idempotent — each call creates a new resource
2. Implement idempotency keys: client sends `Idempotency-Key: <uuid>` header
3. Server stores the key + response for 24 hours
4. On retry with same key, return cached response without creating a new resource

### Exercise 17.D.3 — Debug: 422 vs 400 Confusion

**Symptom:** API returns 422 for malformed JSON (should be 400) and 400 for invalid field values (should be 422).

**Task:**
1. Understand the difference: 400 = syntactically invalid, 422 = syntactically valid but semantically wrong
2. Review your error handlers
3. Fix: FastAPI/Pydantic returns 422 for validation errors by default — this is correct per the JSON:API spec

### Exercise 17.D.4 — Debug: Pagination Off-by-One

**Symptom:** Last page returns one extra item, or first page starts at index 1 instead of 0.

**Task:**
1. Check the offset calculation: `offset = (page - 1) * size`
2. Verify `pages = ceil(total / size)`
3. Fix the calculation and add a test for edge cases (total=0, size=1)

---

## PART E — PRODUCTION SIMULATION

### Scenario: Production CRUD API

Build and operate a production-grade CRUD API:

1. **API design** — Implement all 6 endpoints with proper HTTP semantics
2. **Validation** — Pydantic models with constraints, custom validators
3. **Error handling** — Consistent error responses with appropriate status codes
4. **Pagination** — Offset-based with metadata (total, page, pages)
5. **Rate limiting** — Sliding window per-client rate limiter
6. **Testing** — 100% test coverage with pytest, covering edge cases
7. **Documentation** — OpenAPI spec auto-generated from Pydantic models
8. **Idempotency** — PUT is idempotent; verify with repeated requests
9. **Smoke testing** — curl-based smoke test script for deployment verification

```bash
# Full test suite
uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Smoke test
bash scripts/curl_smoke_test.sh

# OpenAPI spec
curl -s http://localhost:8000/openapi.json | jq .
```

---

## Key Takeaways

1. **PUT replaces, PATCH updates** — Know the difference. Use PUT when the client has the complete resource, PATCH for partial updates.
2. **Idempotency enables reliability** — GET, PUT, DELETE are idempotent; POST is not. Design for safe retries.
3. **Status codes are communication** — Use 201 for creation, 204 for deletion, 404 for not found, 422 for validation.
4. **Always paginate** — Never return unbounded lists. Include total count and page metadata.
5. **Rate limit everything** — Protect your API from abuse and cascading failures.
6. **Test with curl and pytest** — Automated tests for correctness, curl scripts for deployment verification.

---
*Next: [Section 8 — PostgreSQL Production](08-postgresql-production.md)*
