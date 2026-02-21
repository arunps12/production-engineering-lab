# Module 20 — CI/CD Practice

## Goals

- Build a GitHub Actions workflow that tests and validates practice modules
- Run smoke tests for Docker-based services (Postgres, ES, Fuseki)
- Lint and test the FastAPI CRUD app (Module 17)
- Practice "break and fix" CI debugging
- Understand CI pipeline design and optimization

## Prerequisites

- GitHub account with repository access
- Completed modules 14–19 (referenced in CI pipeline)
- Basic GitHub Actions knowledge (Module 6)

## Setup

The CI workflow is at `.github/workflows/practice-ci.yml` in the repo root.

---

## Exercise 20.1 — Understand the CI Pipeline

### Steps

1. Review the workflow:

```bash
cat .github/workflows/practice-ci.yml
```

2. Understand the stages:

| Stage | What It Does | Time |
|-------|-------------|------|
| `lint` | Runs ruff linter on Python code | ~30s |
| `test-crud-api` | Installs deps, runs pytest for Module 17 | ~1min |
| `smoke-postgres` | Starts Postgres, runs schema creation | ~1min |
| `smoke-elasticsearch` | Starts ES, checks health | ~2min |
| `smoke-fuseki` | Starts Fuseki, loads TTL data | ~1min |
| `smoke-crud-api` | Starts CRUD API, runs curl smoke tests | ~1min |

### Key CI Concepts

| Concept | Description |
|---------|-------------|
| **Matrix builds** | Run tests across multiple Python versions |
| **Service containers** | Spin up Postgres/ES/Fuseki as part of CI |
| **Caching** | Cache pip/uv downloads to speed up builds |
| **Artifacts** | Upload test results for debugging |
| **Fail fast** | Stop all jobs if one fails |

---

## Exercise 20.2 — Run CI Locally

You can simulate CI locally using the smoke script:

```bash
bash scripts/ci_smoke.sh
```

This script:
1. Checks Docker is available
2. Starts Postgres and verifies health
3. Starts Elasticsearch and verifies health
4. Starts Fuseki and verifies health
5. Runs Module 17 tests
6. Cleans up all containers

---

## Exercise 20.3 — Break and Fix CI

### Objective

Intentionally break the CI pipeline, then debug and fix it.

### Break 1: Missing Dependency

1. Edit `practice/curriculum/17-rest-api-crud-labs/pyproject.toml`
2. Remove `pydantic[email]` from dependencies
3. Commit and push
4. Watch CI fail with `ModuleNotFoundError`
5. **Fix:** Add the dependency back

### Break 2: Failing Test

1. Edit `practice/curriculum/17-rest-api-crud-labs/tests/test_crud.py`
2. Change an assertion:
   ```python
   assert r.status_code == 201  # change to 200
   ```
3. Commit and push
4. Watch CI fail with `AssertionError`
5. **Fix:** Correct the assertion

### Break 3: Docker Compose Misconfiguration

1. Edit `practice/curriculum/14-postgresql-production-labs/docker-compose.yml`
2. Change `POSTGRES_USER: labuser` to `POSTGRES_USER: wronguser`
3. The smoke test will fail because scripts reference `labuser`
4. **Fix:** Restore the correct username

### Debugging CI Failures

```bash
# 1. Check workflow run logs on GitHub Actions tab
# 2. Look for the FIRST red step
# 3. Read the error message carefully
# 4. Reproduce locally:

cd practice/curriculum/17-rest-api-crud-labs
uv sync
uv run pytest tests/ -v  # Should show same failure

# 5. Fix the issue
# 6. Push the fix
```

---

## Exercise 20.4 — CI Pipeline Optimization

### Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}
```

Saves ~30s per run by caching downloaded packages.

### Parallel Jobs

Independent jobs run in parallel:

```yaml
jobs:
  lint:        # runs in parallel
  test:        # runs in parallel
  smoke-pg:    # runs in parallel
  smoke-es:    # runs in parallel
```

### Conditional Steps

Skip heavy steps on documentation-only changes:

```yaml
on:
  push:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

---

## Deliverables

- [.github/workflows/practice-ci.yml](../../.github/workflows/practice-ci.yml) — CI workflow
- [scripts/ci_smoke.sh](scripts/ci_smoke.sh) — local CI smoke test

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CI takes too long | Add caching, reduce matrix, use `paths` filter |
| Docker not available in CI | Use `services:` or install Docker in the runner |
| Flaky tests | Add retries, increase timeouts, fix race conditions |
| Secrets not available on forks | Use `pull_request_target` or mock secrets |

## Next Steps

- Review all modules 14–20
- Cheatsheets: [SQL vs SPARQL vs ES](../../../docs/cheatsheets/sql_vs_sparql_vs_es.md), [CRUD REST](../../../docs/cheatsheets/crud_rest_put_patch.md)
