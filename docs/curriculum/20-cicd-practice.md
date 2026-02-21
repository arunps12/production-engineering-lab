# SECTION 20 — CI/CD PRACTICE

---

## PART A — CONCEPT EXPLANATION

### What is CI/CD?

**CI (Continuous Integration)** — Automatically build, lint, and test code on every push.
**CD (Continuous Delivery/Deployment)** — Automatically deploy tested code to staging or production.

```
Developer                  CI/CD Pipeline                    Production
    │                                                            │
    │── git push ──→ [Lint] → [Test] → [Build] → [Deploy] ──→  │
    │                  ↓        ↓        ↓          ↓            │
    │               ruff    pytest   Docker     docker compose   │
    │                          ↓                    ↓            │
    │                     coverage            health check       │
```

### Why CI/CD Matters

Without CI/CD:
```
Developer: "It works on my machine"
Production: *broken for 3 hours until someone notices*
```

With CI/CD:
```
Developer: pushes code
CI: "Tests failed — blocked from merging"
Developer: fixes, pushes again
CI: "All green — safe to merge"
CD: automatically deploys to production
```

### GitHub Actions — Core Concepts

GitHub Actions is a CI/CD platform built into GitHub:

**Workflow** — A YAML file in `.github/workflows/` that defines the pipeline:

```yaml
name: CI Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

**Job** — A set of steps that run on the same runner:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest tests/
```

**Step** — A single command or action within a job.

**Action** — A reusable unit (e.g., `actions/checkout@v4`).

**Runner** — The machine that executes the job (GitHub-hosted or self-hosted).

### Pipeline Design

A well-designed CI pipeline has independent, parallel jobs:

```
                    ┌─── lint ──────┐
                    │               │
git push ──→ trigger├─── test ──────├──→ all pass → deploy
                    │               │
                    ├─── smoke-pg ──┤
                    │               │
                    ├─── smoke-es ──┤
                    │               │
                    └─── smoke-api ─┘
```

**Principles:**
- **Independent jobs run in parallel** — Lint and test don't depend on each other
- **Fail fast** — Stop all jobs if one fails
- **Cache dependencies** — Don't re-download packages on every run
- **Use service containers** — Spin up Postgres/Redis as part of CI

### Service Containers

GitHub Actions can run Docker containers alongside your code:

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_PASSWORD: secret
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

The service starts before your steps run, and you connect to it via `localhost`.

### Caching

Cache expensive dependencies to speed up builds:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-uv-
```

**How it works:**
1. First run: no cache → installs everything (~60s)
2. Cache stored with a key based on `pyproject.toml` hash
3. Second run: cache hit → restores cached packages (~5s)
4. When dependencies change: cache miss → new install, new cache

### Matrix Builds

Test across multiple Python versions or OS:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
  fail-fast: true

steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

This creates 3 parallel jobs, one per Python version.

### Artifacts

Upload test reports, coverage, or build outputs:

```yaml
- uses: actions/upload-artifact@v4
  if: always()  # Upload even on failure
  with:
    name: test-results
    path: test-results/
    retention-days: 7
```

### Secrets Management

Never hardcode secrets in workflows:

```yaml
# BAD
env:
  DATABASE_URL: postgresql://admin:password123@db:5432/prod

# GOOD — Use GitHub Secrets
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

Set secrets in: Repository → Settings → Secrets and variables → Actions.

### Local CI Testing

Don't wait for GitHub to test your pipeline — run checks locally first:

```bash
# Lint
ruff check .

# Tests
pytest tests/ -v

# Docker smoke tests
docker compose up -d
curl -s http://localhost:8000/health
docker compose down
```

### Common Beginner Misunderstandings

1. **"CI/CD is just running tests"** — CI includes linting, type checking, security scanning, and integration tests. CD includes deployment, health checks, and rollback.
2. **"I'll fix it in production"** — CI catches bugs before they reach production. Never skip the pipeline.
3. **"Caching makes builds faster"** — Only if the cache key matches. If you cache everything indiscriminately, you get stale dependencies.
4. **"All jobs should be sequential"** — Independent jobs should run in parallel. Only make jobs sequential when there's a real dependency.
5. **"Secrets should be in .env files in the repo"** — Never commit secrets. Use GitHub Secrets or environment-specific secret stores.

---

## PART B — BEGINNER PRACTICE

### Exercise 20.B.1 — Read and Understand the CI Pipeline

Review the GitHub Actions workflow:

```bash
cat .github/workflows/practice-ci.yml
```

Map each job to what it validates:

| Job | What It Tests | Dependencies |
|-----|--------------|--------------|
| `lint` | Python code quality (ruff) | None |
| `test-crud-api` | Module 17 pytest suite | None |
| `smoke-postgres` | Module 14 schema creation | Docker |
| `smoke-elasticsearch` | Module 15 ES health | Docker |
| `smoke-fuseki` | Module 16 data loading | Docker |
| `smoke-crud-api` | Module 17 API endpoints | Docker |

**Practice file:** `.github/workflows/practice-ci.yml`

### Exercise 20.B.2 — Run CI Checks Locally

Run the same checks that CI runs, on your local machine:

```bash
cd practice/curriculum/20-ci-cd-practice
bash scripts/ci_smoke.sh
```

The script:
1. Checks Docker is available
2. Starts Postgres and runs schema scripts
3. Starts Elasticsearch and checks health
4. Starts Fuseki and loads data
5. Runs Module 17 tests
6. Cleans up containers

**Practice file:** `practice/curriculum/20-ci-cd-practice/scripts/ci_smoke.sh`

### Exercise 20.B.3 — Set Up Linting

Install and run `ruff`:

```bash
# Install
pip install ruff

# Check all Python files
ruff check practice/curriculum/17-rest-api-crud-labs/

# Auto-fix issues
ruff check --fix practice/curriculum/17-rest-api-crud-labs/

# Format
ruff format practice/curriculum/17-rest-api-crud-labs/
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 20.C.1 — Break and Fix CI

Intentionally break the CI pipeline and practice debugging:

**Break 1 — Missing dependency:**
```bash
# Remove pydantic[email] from pyproject.toml
# Commit and push
# Watch CI fail with ModuleNotFoundError
# Fix: add the dependency back
```

**Break 2 — Failing test:**
```python
# Change an assertion in test_crud.py
assert r.status_code == 200  # Should be 201
# Watch CI fail with AssertionError
# Fix: correct the assertion
```

**Break 3 — Docker misconfiguration:**
```yaml
# Change POSTGRES_USER in docker-compose.yml
# Smoke test fails because scripts use the original user
# Fix: restore the correct username
```

### Exercise 20.C.2 — Add a New CI Job

Add a job that validates the Docker Compose files:

```yaml
validate-compose:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Validate compose files
      run: |
        for f in practice/curriculum/*/docker-compose.yml; do
          echo "Validating $f..."
          docker compose -f "$f" config --quiet
        done
```

### Exercise 20.C.3 — CI Pipeline Optimization

Measure and optimize build times:

```yaml
# 1. Add caching
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}

# 2. Run independent jobs in parallel (already done)

# 3. Use conditional steps
- name: Run integration tests
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  run: bash scripts/integration_tests.sh
```

### Exercise 20.C.4 — Coverage Reports

Add test coverage to CI:

```bash
# Local
uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# In CI — upload as artifact
- name: Run tests with coverage
  run: uv run pytest tests/ --cov=src --cov-report=xml
- uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: coverage.xml
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 20.D.1 — Debug: CI Passes Locally, Fails in CI

**Symptom:** Tests pass on your machine but fail in GitHub Actions.

**Task:**
1. Check Python version differences (local vs CI runner)
2. Check for OS-dependent behavior (macOS vs Linux)
3. Check for hardcoded paths or environment-specific assumptions
4. Check for time-dependent tests (timezone, timestamps)
5. Fix: Make tests environment-agnostic

### Exercise 20.D.2 — Debug: Service Container Not Ready

**Symptom:** Tests fail with `connection refused` to Postgres, even though the service is defined.

**Task:**
1. Service containers need time to initialize
2. Add a `wait-for` step:
   ```yaml
   - name: Wait for Postgres
     run: |
       for i in $(seq 1 30); do
         pg_isready -h localhost && break
         sleep 1
       done
   ```
3. Or use the `options` health check in the service definition

### Exercise 20.D.3 — Debug: Cache Causing Stale Dependencies

**Symptom:** A new dependency was added to `pyproject.toml` but CI uses the cached version without it.

**Task:**
1. Cache key includes `hashFiles('**/pyproject.toml')` — it should bust automatically
2. Check if the correct file is hashed
3. Manual fix: change cache key prefix or delete cache on GitHub (Settings → Actions → Caches)

### Exercise 20.D.4 — Debug: Flaky Tests

**Symptom:** Tests pass 80% of the time, fail randomly.

**Task:**
1. Look for: race conditions, sleep-based timing, unordered results, external dependencies
2. Run tests in a loop to reproduce: `for i in $(seq 1 10); do pytest tests/ || break; done`
3. Fix: Use deterministic assertions, mock external calls, avoid shared state

---

## PART E — PRODUCTION SIMULATION

### Scenario: Complete CI/CD Pipeline

Build and operate a complete CI/CD pipeline for modules 14-20:

1. **Lint** — ruff checks on all Python code
2. **Unit tests** — pytest with coverage for Module 17
3. **Integration tests** — Docker-based smoke tests for Postgres, ES, Fuseki
4. **API tests** — Start the CRUD API and run curl smoke tests
5. **Compose validation** — Validate all docker-compose.yml files
6. **Coverage gate** — Fail if test coverage drops below 80%
7. **Artifact upload** — Save test results and coverage reports

```yaml
# Production CI/CD pipeline structure
name: Production CI/CD

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:          # Fast feedback — ~30s
  test:          # Unit + coverage — ~1min
  smoke-db:      # Postgres smoke — ~1min
  smoke-search:  # ES smoke — ~2min
  smoke-api:     # API smoke — ~1min
  deploy:        # Only on main, after all pass
    needs: [lint, test, smoke-db, smoke-search, smoke-api]
    if: github.ref == 'refs/heads/main'
```

Advanced extensions:
8. **Notifications** — Send Slack/email on failure
9. **Branch protection** — Require CI to pass before merging
10. **Deployment environments** — Deploy to staging first, then production with approval

---

## Key Takeaways

1. **CI catches bugs before production** — Every push should run lint, test, and integration checks.
2. **Independent jobs run in parallel** — Don't serialize jobs that don't depend on each other.
3. **Cache dependencies** — Saves 30-60 seconds per build. Use file hashes as cache keys.
4. **Test locally first** — Don't use CI as your only test environment. Run the same checks locally.
5. **Service containers enable integration tests** — Spin up Postgres/ES/Redis as part of CI.
6. **Secrets never go in code** — Use GitHub Secrets or environment-specific secret stores.

---
*Previous: [Section 19 — Ansible Practice](19-ansible-practice.md)*
