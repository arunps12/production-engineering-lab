# Module 17 — REST API CRUD Labs (FastAPI)

## Goals

- Build a complete REST CRUD API with FastAPI
- Implement proper HTTP semantics (status codes, error shapes)
- Understand PUT vs PATCH and idempotency
- Add pagination, rate limiting, and input validation
- Test with pytest and verify with curl

## Prerequisites

- Python 3.11+ with `uv`
- Completed modules 3–4 (REST API design, FastAPI basics)

## Setup

```bash
cd practice/curriculum/17-rest-api-crud-labs

# Create virtual environment and install dependencies
uv sync

# Run the app
uv run uvicorn src.crud_api.main:app --reload --port 8000
```

OpenAPI docs: http://localhost:8000/docs

---

## API Endpoints

| Method | Path | Description | Status Codes |
|--------|------|-------------|-------------|
| POST | /users | Create a user | 201, 422, 429 |
| GET | /users | List users (paginated) | 200, 429 |
| GET | /users/{id} | Get single user | 200, 404 |
| PUT | /users/{id} | Full replace | 200, 404, 422 |
| PATCH | /users/{id} | Partial update | 200, 404, 422 |
| DELETE | /users/{id} | Delete user | 204, 404 |

---

## Exercise 17.1 — Run the App and Explore

### Steps

1. Start the server:

```bash
uv run uvicorn src.crud_api.main:app --reload --port 8000
```

2. Open the interactive docs: http://localhost:8000/docs

3. Try each endpoint via the Swagger UI.

4. Run the smoke test:

```bash
bash scripts/curl_smoke_test.sh
```

---

## Exercise 17.2 — PUT vs PATCH Deep Dive

### PUT (Full Replace)

PUT replaces the **entire resource**. All fields must be provided.

```bash
# PUT requires ALL fields
curl -X PUT http://localhost:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"username": "alice_updated", "email": "alice_new@example.com", "full_name": "Alice Johnson Updated"}'
```

If you omit a field, it should fail validation (422).

### PATCH (Partial Update)

PATCH updates **only the provided fields**. Omitted fields remain unchanged.

```bash
# PATCH only changes the specified field
curl -X PATCH http://localhost:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"full_name": "Alice J."}'
```

### Idempotency

| Method | Idempotent? | Explanation |
|--------|------------|-------------|
| GET | Yes | Multiple identical requests return the same result |
| PUT | Yes | Same PUT request always produces the same resource state |
| PATCH | Depends | If patch is "set field X to value Y" → idempotent. If "increment X" → not idempotent |
| DELETE | Yes | Deleting an already-deleted resource returns 404 (same end state) |
| POST | No | Each POST creates a new resource |

### SQL CRUD Mapping

| REST | SQL | HTTP Method | Status Code |
|------|-----|-------------|-------------|
| Create | INSERT INTO | POST | 201 Created |
| Read | SELECT | GET | 200 OK |
| Update (full) | UPDATE SET (all cols) | PUT | 200 OK |
| Update (partial) | UPDATE SET (some cols) | PATCH | 200 OK |
| Delete | DELETE FROM | DELETE | 204 No Content |

---

## Exercise 17.3 — Pagination

The GET /users endpoint supports pagination:

```bash
# First page (default: 10 per page)
curl -s "http://localhost:8000/users?page=1&size=5" | jq .

# Second page
curl -s "http://localhost:8000/users?page=2&size=5" | jq .
```

Response includes pagination metadata:

```json
{
  "items": [...],
  "total": 15,
  "page": 1,
  "size": 5,
  "pages": 3
}
```

---

## Exercise 17.4 — Error Handling

All errors return a consistent shape:

```json
{
  "detail": "User not found",
  "status_code": 404
}
```

Test error cases:

```bash
# 404 — user not found
curl -s http://localhost:8000/users/9999 | jq .

# 422 — validation error (invalid email)
curl -s -X POST http://localhost:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"username": "test", "email": "not-an-email", "full_name": "Test"}' | jq .

# 422 — PUT with missing required field
curl -s -X PUT http://localhost:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"username": "test"}' | jq .
```

---

## Exercise 17.5 — Rate Limiting

The API includes a simple in-memory rate limiter (100 requests/minute per client).

```bash
# Rapid-fire requests to trigger rate limit
for i in $(seq 1 110); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/users)
  if [ "$STATUS" = "429" ]; then
    echo "Rate limited at request $i"
    break
  fi
done
```

---

## Exercise 17.6 — Run Tests

```bash
uv run pytest tests/ -v
```

Expected: all tests pass.

```bash
# With coverage
uv run pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Project Structure

```
17-rest-api-crud-labs/
├── pyproject.toml
├── README.md
├── src/
│   └── crud_api/
│       ├── __init__.py
│       ├── main.py          # FastAPI app + middleware
│       ├── routes.py        # CRUD endpoints
│       ├── schemas.py       # Pydantic models
│       ├── database.py      # In-memory store
│       └── rate_limiter.py  # Simple rate limiter
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_crud.py
│   └── test_rate_limiter.py
└── scripts/
    └── curl_smoke_test.sh
```

---

## Cleanup

Stop the server with Ctrl+C.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `uv sync` to install dependencies |
| Port 8000 in use | Use `--port 8001` or kill the existing process |
| Tests fail | Ensure no server is running (tests use TestClient) |

## Next Steps

- Module 18: Docker Debug Labs
- Cheatsheet: [CRUD REST PUT vs PATCH](../../../docs/cheatsheets/crud_rest_put_patch.md)
