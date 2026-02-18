# SECTION 5 — TESTING WITH PYTEST

---

## PART A — CONCEPT EXPLANATION

### Why Testing is a Non-Negotiable Skill

Testing is not optional in production engineering. It's the foundation of:
- **Confidence** — Deploy without fear of breaking things
- **Documentation** — Tests show how code is supposed to work
- **Refactoring** — Change internals safely when tests pass
- **CI/CD** — Automated pipelines rely on automated tests

### The Testing Pyramid

```
        /  E2E Tests  \          ← Few, slow, expensive
       / Integration    \        ← Medium amount
      /   Unit Tests     \       ← Many, fast, cheap
     /_____________________\
```

- **Unit tests** — Test one function/class in isolation
- **Integration tests** — Test components working together
- **End-to-end (E2E) tests** — Test the full system like a user would

### pytest Fundamentals

pytest is Python's de facto testing framework. It's simple, powerful, and extensible.

```python
# test_math.py
def test_addition():
    assert 1 + 1 == 2

def test_string_upper():
    assert "hello".upper() == "HELLO"

def test_list_append():
    items = [1, 2]
    items.append(3)
    assert items == [1, 2, 3]
    assert len(items) == 3
```

```bash
pytest test_math.py -v
```

**Key principles:**
- Test files start with `test_` or end with `_test.py`
- Test functions start with `test_`
- Use plain `assert` statements (pytest rewrites them for better error messages)
- Each test should be independent (no shared state)

### Fixtures — Setup and Teardown

Fixtures provide test data and resources:

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Alice", "email": "alice@test.com", "age": 30}

@pytest.fixture
def database():
    db = create_database()       # Setup
    yield db                     # Provide to test
    db.close()                   # Teardown (runs after test)

def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"

def test_db_insert(database):
    database.insert({"id": 1})
    assert database.count() == 1
```

**Fixture scopes:**
- `function` (default) — Run for each test
- `class` — Run once per test class
- `module` — Run once per test file
- `session` — Run once for entire test session

### Mocking — Isolating What You Test

When testing code that calls external services, databases, or APIs, mock the dependencies:

```python
from unittest.mock import Mock, patch

def get_user_from_api(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

def test_get_user():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"name": "Alice"}
        user = get_user_from_api(1)
        assert user["name"] == "Alice"
        mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### Parametrize — Many Inputs, One Test

```python
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
    (-1, 1),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### Test-Driven Development (TDD)

The TDD cycle:
1. **Red** — Write a failing test
2. **Green** — Write minimum code to pass
3. **Refactor** — Clean up, keeping tests green

```python
# Step 1: Write the test first
def test_validate_email():
    assert validate_email("user@example.com") == True
    assert validate_email("invalid") == False
    assert validate_email("") == False

# Step 2: Write the implementation
def validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1] and len(email) > 5

# Step 3: Refactor if needed
```

### Common Beginner Misunderstandings

1. **"Testing slows me down"** — It slows you down now, saves you 10x later. Debugging production issues without tests is far slower.
2. **"100% coverage means no bugs"** — Coverage measures lines executed, not correctness. You can have 100% coverage and still have logic errors.
3. **"Mock everything"** — Over-mocking makes tests fragile and meaningless. Mock external boundaries (APIs, databases), not internal logic.
4. **"Tests should be complex"** — Simple tests are better. If a test is hard to write, the code probably needs refactoring.
5. **"I only need unit tests"** — Unit tests catch individual bugs. Integration tests catch wiring bugs. You need both.

---

## PART B — BEGINNER PRACTICE

### Exercise 5.B.1 — First Test File

Write tests for a `calculator` module:
```python
# calculator.py
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

Write at least 8 tests covering normal and edge cases.

### Exercise 5.B.2 — Testing with Assertions

Practice different assertion patterns:
```python
assert result == expected           # Equality
assert result != unexpected         # Inequality
assert result > 0                   # Comparison
assert item in collection           # Membership
assert isinstance(obj, MyClass)     # Type check
assert result is None               # Identity
assert len(items) == 3              # Length

# Testing exceptions:
with pytest.raises(ValueError):
    divide(1, 0)

with pytest.raises(ValueError, match="Cannot divide by zero"):
    divide(1, 0)
```

### Exercise 5.B.3 — Fixtures for Test Data

Create fixtures for:
1. A sample user dictionary
2. A list of products
3. A temporary file with test content
4. A configured logger

### Exercise 5.B.4 — Parametrize Tests

Use `@pytest.mark.parametrize` to test:
1. A function that converts temperatures (F → C, C → F)
2. A function that validates passwords (various invalid/valid inputs)
3. A function that formats names (different cases)

### Exercise 5.B.5 — Test Organization

Organize tests into proper structure:
```
tests/
├── conftest.py          ← Shared fixtures
├── test_calculator.py
├── test_models.py
├── test_utils.py
└── integration/
    └── test_api.py
```

### Exercise 5.B.6 — Run Tests with Options

```bash
pytest                              # Run all tests
pytest test_file.py                 # Run one file
pytest test_file.py::test_function  # Run one test
pytest -v                           # Verbose output
pytest -x                           # Stop on first failure
pytest --tb=short                   # Short traceback
pytest -k "email"                   # Run tests matching keyword
pytest --lf                         # Rerun last failures
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 5.C.1 — Mocking External Services

Test a function that calls an external API without actually making HTTP requests.

### Exercise 5.C.2 — Testing FastAPI Endpoints

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_user():
    response = client.post("/users", json={"name": "Alice", "email": "a@b.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
```

### Exercise 5.C.3 — Fixture Composition

Create fixtures that depend on other fixtures:
```python
@pytest.fixture
def db():
    database = create_test_database()
    yield database
    database.drop()

@pytest.fixture
def user(db):
    return db.create_user(name="Alice")

@pytest.fixture
def auth_token(user):
    return create_token(user.id)

def test_authenticated_request(auth_token):
    # auth_token depends on user, which depends on db
    ...
```

### Exercise 5.C.4 — Test Coverage

```bash
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=html    # Open htmlcov/index.html
```

Find untested code paths and write tests for them.

### Exercise 5.C.5 — Testing Exceptions and Edge Cases

Write tests for:
1. Empty input
2. None input
3. Very large numbers
4. Unicode strings
5. Concurrent access
6. Timeout scenarios

### Exercise 5.C.6 — TDD Exercise

Build a `PasswordValidator` class using TDD:
1. Write tests first for all rules (length, uppercase, digit, special char)
2. Implement the class to pass all tests
3. Refactor without breaking tests

---

## PART D — ADVANCED DEBUG LAB

### Exercise 5.D.1 — Debug: Test Passes Alone, Fails Together

Symptom: `pytest test_a.py` passes, `pytest` (all tests) fails.
Cause: Tests share state (global variable, database, file).
Task: Find and fix the shared state leak.

### Exercise 5.D.2 — Debug: Flaky Test

Symptom: Test passes most of the time but occasionally fails.
Cause: Time-dependent, random data, or race condition.
Task: Make the test deterministic.

### Exercise 5.D.3 — Debug: Mock Not Working

Symptom: Mock is applied but the real function still runs.
Cause: Patching wrong import path (must patch where it's used, not where it's defined).
Task: Fix the `patch()` target.

### Exercise 5.D.4 — Debug: Coverage Lies

Symptom: 95% coverage but a bug in production.
Task: Find the untested logic path that coverage missed (executed line ≠ tested behavior).

---

## PART E — PRODUCTION SIMULATION

### Scenario: Complete Test Suite

Build a complete test suite for your production service:
1. **Unit tests** — All business logic functions (~20 tests)
2. **Integration tests** — API endpoint tests with TestClient (~10 tests)
3. **Fixtures** — Shared test data in `conftest.py`
4. **Mocks** — External service calls mocked
5. **Parametrize** — Edge cases for validation
6. **Coverage** — Achieve >80% coverage
7. **CI integration** — Tests run in GitHub Actions

```bash
pytest tests/ -v --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## Key Takeaways

1. **Tests are code documentation** — A well-tested codebase tells you exactly what the code does.
2. **Use fixtures to eliminate duplication** — Shared setup belongs in fixtures, not repeated in every test.
3. **Mock at boundaries, not internals** — Mock external APIs and databases. Don't mock your own logic.
4. **Parametrize for edge cases** — One test function can verify dozens of inputs.
5. **Coverage is a guide, not a goal** — Aim for meaningful tests, not 100% coverage.
6. **TDD works** — Writing tests first leads to cleaner, more testable code.

---
*Next: [Section 6 — Concurrency & Async Python](06-concurrency-async.md)*
