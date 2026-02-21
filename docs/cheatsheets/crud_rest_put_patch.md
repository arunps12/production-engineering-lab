# CRUD ↔ REST ↔ SQL ↔ SPARQL — Cheatsheet

## CRUD to REST Mapping

| CRUD | HTTP Method | Path | Status Code | Idempotent? |
|------|------------|------|-------------|-------------|
| **C**reate | POST | /resources | 201 Created | No |
| **R**ead (all) | GET | /resources | 200 OK | Yes |
| **R**ead (one) | GET | /resources/{id} | 200 OK | Yes |
| **U**pdate (full) | PUT | /resources/{id} | 200 OK | Yes |
| **U**pdate (partial) | PATCH | /resources/{id} | 200 OK | Depends |
| **D**elete | DELETE | /resources/{id} | 204 No Content | Yes |

---

## PUT vs PATCH

### PUT — Full Replace

- **All fields** must be provided
- Missing fields are treated as intentional removals
- **Idempotent**: same PUT request always produces the same resource state

```http
PUT /users/1
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@example.com",
  "full_name": "Alice Johnson"
}
```

**SQL equivalent:**
```sql
UPDATE users
SET username = 'alice',
    email = 'alice@example.com',
    full_name = 'Alice Johnson',
    updated_at = NOW()
WHERE id = 1;
```

### PATCH — Partial Update

- Only **provided fields** are updated
- Omitted fields remain unchanged
- **Idempotent if** the patch is "set X to value" (not "increment X")

```http
PATCH /users/1
Content-Type: application/json

{
  "full_name": "Alice J."
}
```

**SQL equivalent:**
```sql
UPDATE users
SET full_name = 'Alice J.',
    updated_at = NOW()
WHERE id = 1;
```

### When to Use Each

| Scenario | Use |
|----------|-----|
| Client has the complete resource | PUT |
| Client updates one field | PATCH |
| Form submission (all fields) | PUT |
| Toggle a boolean flag | PATCH |
| API with many optional fields | PATCH |
| Simple replacement semantics | PUT |

---

## Idempotency Deep Dive

**Idempotent** = Multiple identical requests produce the same result as a single request.

| Method | Idempotent? | Explanation |
|--------|------------|-------------|
| GET | Yes | Reading doesn't change state |
| PUT | Yes | Same body → same resource state |
| DELETE | Yes | Resource is gone after first call; subsequent calls return 404 but end state is the same |
| PATCH | **Depends** | `{"name": "Alice"}` → idempotent; `{"views": "+1"}` → not idempotent |
| POST | No | Each call creates a new resource |

### Safe vs Idempotent

| Property | GET | POST | PUT | PATCH | DELETE |
|----------|-----|------|-----|-------|--------|
| Safe (no side effects) | Yes | No | No | No | No |
| Idempotent | Yes | No | Yes | Depends | Yes |

---

## CRUD in SQL vs SPARQL

### Create

**SQL:**
```sql
INSERT INTO books (title, author, year)
VALUES ('Clean Code', 'Robert C. Martin', 2008);
```

**SPARQL:**
```sparql
PREFIX ex: <http://example.org/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX schema: <http://schema.org/>

INSERT DATA {
    ex:book/3 a schema:Book ;
              dct:title "Clean Code" ;
              schema:author "Robert C. Martin" ;
              schema:datePublished "2008" .
}
```

### Read

**SQL:**
```sql
SELECT title, author FROM books WHERE year > 2016;
```

**SPARQL:**
```sparql
SELECT ?title ?author
WHERE {
    ?book dct:title ?title ;
          schema:author ?author ;
          schema:datePublished ?year .
    FILTER (?year > "2016")
}
```

### Update

**SQL:**
```sql
UPDATE books SET title = 'Clean Code (2nd Ed)' WHERE id = 3;
```

**SPARQL:**
```sparql
DELETE { ex:book/3 dct:title ?oldTitle }
INSERT { ex:book/3 dct:title "Clean Code (2nd Ed)" }
WHERE  { ex:book/3 dct:title ?oldTitle }
```

Note: SPARQL updates use DELETE/INSERT pattern (no direct UPDATE).

### Delete

**SQL:**
```sql
DELETE FROM books WHERE id = 3;
```

**SPARQL:**
```sparql
-- Delete specific triples
DELETE WHERE { ex:book/3 ?p ?o }
```

---

## Status Codes Reference

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | GET, PUT, PATCH success |
| 201 | Created | POST success (include Location header) |
| 204 | No Content | DELETE success (empty body) |
| 400 | Bad Request | Malformed request body |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource / state conflict |
| 422 | Unprocessable Entity | Valid JSON but invalid data |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server failure |

---

## Error Response Shape

Use a consistent error format across your API:

```json
{
  "detail": "User not found",
  "status_code": 404
}
```

For validation errors (422):

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```
