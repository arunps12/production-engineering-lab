# SECTION 6 — CI/CD THEORY & PRACTICE

---

## PART A — CONCEPT EXPLANATION

### What is CI (Continuous Integration)?

**CI** is the practice of automatically building and testing your code **every time someone pushes a change**. The goal: catch bugs within minutes, not days.

```
Developer pushes code
        ↓
CI server detects the push
        ↓
┌────────────────────────────┐
│  CI Pipeline               │
│  1. Clone the repository   │
│  2. Set up environment     │
│  3. Install dependencies   │
│  4. Run linter/formatter   │
│  5. Run unit tests         │
│  6. Run integration tests  │
│  7. Build Docker image     │
│  8. Report results         │
└────────────────────────────┘
        ↓
✓ All passed → merge allowed
✗ Any failed → merge blocked
```

**Why CI matters:** Without CI, you merge broken code. Someone else pulls it. Their work now fails. They spend hours debugging YOUR bug. CI prevents this by answering one question: **"Does this change break anything?"**

**What CI is NOT:**
- A deployment tool (that's CD)
- A replacement for local testing (always test before pushing)
- Optional for small teams (it's even MORE important for small teams)

### What is CD (Continuous Deployment/Delivery)?

**CD** extends CI to automatically deploy your code to production (or staging):

```
Continuous Delivery:
  Code pushed → CI passes → Artifact ready → MANUAL approval → Deploy

Continuous Deployment:
  Code pushed → CI passes → Artifact ready → AUTO deploy → Production
```

**The distinction matters:**
- **Delivery**: you can deploy at any time, but a human decides when
- **Deployment**: every passing commit goes to production automatically

Most teams start with **Continuous Delivery** and graduate to **Continuous Deployment** as they build confidence in their test suite.

### Why Pipelines Fail

The most common CI failure categories:

| Category | Cause | Fix |
|---|---|---|
| **Environment mismatch** | CI uses Python 3.12, project needs 3.11 | Pin Python version in CI config |
| **Missing dependencies** | System library not installed in CI image | Add `apt-get install` step |
| **Stale lockfile** | `pyproject.toml` changed but `uv.lock` wasn't updated | Run `uv lock --check` in CI |
| **Flaky tests** | Tests depend on timing, network, or random data | Isolate tests, use mocks |
| **Docker auth** | CI can't pull base images or push to registry | Configure secrets/tokens |
| **Resource limits** | CI runner runs out of memory during build | Optimize build or use larger runner |
| **Cache corruption** | Cached dependencies are stale or corrupt | Clear CI cache |

### What is an Artifact?

An **artifact** is any output from a CI/CD pipeline that can be deployed or shared:

| Artifact Type | Example |
|---|---|
| Docker image | `ghcr.io/myorg/myapp:v1.2.3` |
| Python wheel | `appcore-0.1.0-py3-none-any.whl` |
| Test report | `test-results.xml` |
| Coverage report | `coverage.html` |
| Binary | compiled executable |

**Best practice:** Tag artifacts with:
- Git commit SHA (`myapp:abc1234`)
- Semantic version (`myapp:v1.2.3`)
- NEVER use `:latest` in production (it's mutable and unpredictable)

### What is Environment Mismatch?

Environment mismatch = **your CI/CD environment differs from your development or production environment.**

```
Your laptop:        Python 3.12.1, Ubuntu 24.04, libssl 3.0
CI runner:          Python 3.11.8, Ubuntu 22.04, libssl 1.1
Docker image:       Python 3.11.7, Debian Bookworm, libssl 3.0
Production server:  Python 3.11.5, Amazon Linux 2, libssl 1.1
```

**Result:** Code that passes locally fails in CI. Code that passes in CI fails in production.

**Solutions:**
1. **Docker**: Package your exact environment
2. **Lockfiles**: Pin every dependency version (`uv.lock`)
3. **CI configuration**: Explicitly specify Python version, OS, etc.
4. **Test in Docker locally**: `docker build . && docker run`

### Why "Works on My Machine" Happens

The root causes:

1. **Implicit dependencies**: Your system has `libmagic` installed globally, CI doesn't
2. **PATH differences**: Your shell has `~/.local/bin` in PATH, CI doesn't
3. **Environment variables**: You have `DATABASE_URL` set locally, CI doesn't
4. **File system differences**: macOS is case-insensitive, Linux is case-sensitive → `import MyModule` works on Mac, fails on Linux
5. **Cached state**: Your `.venv` has old packages that happen to work, fresh install reveals conflicts
6. **Network access**: Your machine can reach internal services, CI runner can't

**The only reliable test:** Destroy your local environment and rebuild from scratch:
```bash
rm -rf .venv
uv sync --frozen
uv run pytest tests/ -v
```
If this fails, it'll fail in CI too.

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "CI is just running pytest" | CI includes linting, type checking, security scanning, building artifacts |
| "If it passes locally, it'll pass in CI" | Local and CI environments are never identical without Docker |
| "CI is slow, I'll skip it" | CI catches bugs that save hours of debugging later |
| "I don't need CD for side projects" | CD practice translates directly to job skills |
| "Secrets are safe in the repo if it's private" | Secrets in code = compromised. Use CI secret management |
| "`:latest` tag is fine for production" | `:latest` is mutable — it can change from under you |

---

## PART B — BEGINNER PRACTICE

### Exercise 6.B.1 — Create the CI Workflow

```bash
mkdir -p .github/workflows
```

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.11

      - name: Verify lockfile is up to date
        run: uv lock --check

      - name: Install dependencies
        run: uv sync --frozen --dev

      - name: Run tests
        run: uv run pytest tests/ -v --tb=short

  lint:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --frozen --dev

      - name: Run ruff (linter)
        run: uv run ruff check src/ tests/

      - name: Run ruff (formatter check)
        run: uv run ruff format --check src/ tests/
```

### Exercise 6.B.2 — Add Linting Dependencies

```bash
cd ~/Projects/practical-production-service

# Add ruff for linting and formatting
uv add --dev ruff

# Configure ruff in pyproject.toml
```

Add to `pyproject.toml`:
```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.ruff.format]
quote-style = "double"
```

```bash
# Test locally (same commands CI will run)
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
```

### Exercise 6.B.3 — Understand the Workflow Syntax

```yaml
# Line-by-line explanation:

name: CI               # Name shown in GitHub UI

on:                     # Triggers
  push:
    branches: [main]    # Run on pushes to main
  pull_request:
    branches: [main]    # Run on PRs targeting main

jobs:                   # Parallel job definitions
  test:                 # Job name
    runs-on: ubuntu-latest  # Runner OS
    
    steps:              # Sequential steps within the job
      - name: Checkout  # Human-readable step name
        uses: actions/checkout@v4  # Predefined action (from marketplace)

      - name: Run tests
        run: pytest     # Shell command
```

**Key concepts:**
- **Jobs** run in parallel by default
- **Steps** within a job run sequentially
- **`uses`** runs a pre-built action
- **`run`** runs a shell command
- **`on`** defines when the workflow triggers

### Exercise 6.B.4 — Add a Docker Build Job

```yaml
# Add to .github/workflows/ci.yml

  docker:
    runs-on: ubuntu-latest
    needs: [test, lint]  # Only run after test and lint pass
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        run: docker build -t production-service:ci .

      - name: Test Docker image starts
        run: |
          docker run -d --name ci-test -p 8000:8000 production-service:ci
          sleep 5
          curl -f http://localhost:8000/health
          docker stop ci-test
          docker rm ci-test
```

### Exercise 6.B.5 — Simulate CI Locally

```bash
# Reproduce exactly what CI does, locally:

# 1. Start from clean state
rm -rf .venv

# 2. Check lockfile
uv lock --check

# 3. Install deps
uv sync --frozen --dev

# 4. Lint
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# 5. Test
uv run pytest tests/ -v --tb=short

# 6. Docker build
docker build -t production-service:local .

# 7. Smoke test
docker run -d --name local-test -p 8000:8000 production-service:local
sleep 3
curl -f http://localhost:8000/health && echo " ✓ Health check passed"
docker stop local-test && docker rm local-test

echo "=== All CI checks passed locally ==="
```

### Exercise 6.B.6 — Write a CI Simulation Script

```bash
cat > scripts/run_ci_local.sh <<'SCRIPT'
#!/bin/bash
set -euo pipefail

echo "========================================"
echo "  LOCAL CI SIMULATION"
echo "  $(date)"
echo "========================================"

ERRORS=0

run_step() {
    local step_name="$1"
    shift
    echo -e "\n--- $step_name ---"
    if "$@"; then
        echo "✓ $step_name PASSED"
    else
        echo "✗ $step_name FAILED"
        ERRORS=$((ERRORS + 1))
    fi
}

run_step "Lockfile check" uv lock --check
run_step "Install deps" uv sync --frozen --dev
run_step "Lint" uv run ruff check src/ tests/
run_step "Format" uv run ruff format --check src/ tests/
run_step "Tests" uv run pytest tests/ -v --tb=short

echo -e "\n========================================"
if [[ $ERRORS -gt 0 ]]; then
    echo "  RESULT: ✗ FAILED ($ERRORS issues)"
    exit 1
else
    echo "  RESULT: ✓ ALL CHECKS PASSED"
fi
echo "========================================"
SCRIPT
chmod +x scripts/run_ci_local.sh

# Run it
./scripts/run_ci_local.sh
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 6.C.1 — Add Caching to Speed Up CI

```yaml
# Improved CI with caching
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4

      - name: Set up uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true  # Cache uv packages between runs

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --frozen --dev

      - name: Verify lockfile
        run: uv lock --check

      - name: Lint
        run: |
          uv run ruff check src/ tests/
          uv run ruff format --check src/ tests/

      - name: Test
        run: uv run pytest tests/ -v --tb=short --junitxml=test-results.xml

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()  # Upload even if tests fail
        with:
          name: test-results
          path: test-results.xml
```

### Exercise 6.C.2 — Add a Matrix Strategy

```yaml
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --frozen --dev

      - name: Test
        run: uv run pytest tests/ -v
```

This runs tests on **both Python 3.11 and 3.12** in parallel. If your code works on one but not the other, you'll know immediately.

### Exercise 6.C.3 — Push Docker Image to Registry

```yaml
  docker:
    runs-on: ubuntu-latest
    needs: [test]
    if: github.ref == 'refs/heads/main'  # Only on main branch
    
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
```

### Exercise 6.C.4 — Add CD: Deploy to Remote Server

```yaml
  deploy:
    runs-on: ubuntu-latest
    needs: [docker]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to server via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            # Pull the new image
            docker pull ghcr.io/${{ github.repository }}:${{ github.sha }}
            
            # Stop the old container
            docker stop production-service || true
            docker rm production-service || true
            
            # Start the new container
            docker run -d \
              --name production-service \
              --restart unless-stopped \
              -p 8000:8000 \
              -e APP_VERSION=${{ github.sha }} \
              ghcr.io/${{ github.repository }}:${{ github.sha }}
            
            # Verify it's healthy
            sleep 10
            curl -f http://localhost:8000/health || exit 1
            
            echo "Deployment successful: ${{ github.sha }}"
```

**Required secrets** (set in GitHub repo settings → Secrets):
- `DEPLOY_HOST` — server IP address
- `DEPLOY_USER` — SSH username
- `DEPLOY_SSH_KEY` — SSH private key

### Exercise 6.C.5 — Git Tagging for Releases

```bash
# Create a version tag
git tag v0.1.0
git push origin v0.1.0

# List all tags
git tag -l

# Create an annotated tag (with message)
git tag -a v0.2.0 -m "Release 0.2.0: Added prediction endpoint"
git push origin v0.2.0
```

Add a release workflow:

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4

      - name: Extract version from tag
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push tagged image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ steps.version.outputs.VERSION }}
            ghcr.io/${{ github.repository }}:latest
```

### Exercise 6.C.6 — Branch Protection Rules

Document the recommended GitHub settings:

```markdown
## Branch Protection for `main`

Enable in: Settings → Branches → Add branch protection rule

Required settings:
- [x] Require a pull request before merging
- [x] Require status checks to pass before merging
  - Required checks: test, lint
- [x] Require branches to be up to date before merging
- [x] Do not allow bypassing the above settings
```

This ensures:
1. Nobody can push directly to main
2. Every change must pass CI before merge
3. No "I'll fix CI later" commits

---

## PART D — ADVANCED DEBUG LAB

### Exercise 6.D.1 — Debug: CI Passes but CD Fails

**Scenario:** Tests pass in CI, Docker build succeeds, but the deployed service crashes.

**Common causes and diagnostics:**

```bash
# 1. Different Python version in CI vs Docker
# CI: uv python install 3.12
# Dockerfile: FROM python:3.11-slim
# Fix: Use the same Python version everywhere

# 2. Missing environment variables in production
# CI has no env vars (tests use defaults)
# Production needs DATABASE_URL, API_KEY, etc.
# Fix: Check docker run -e flags or docker-compose environment section

# 3. Port mismatch
# Dockerfile: EXPOSE 8000
# docker run: -p 9000:8000  ← mapped to 9000 on host
# Health check: curl localhost:8000  ← checking wrong port on host
# Fix: Use consistent port mapping

# 4. Build args not passed during deployment
# Local: docker build --build-arg VERSION=1.0 .
# CI: docker build .  ← VERSION arg not passed
# Fix: Set defaults in Dockerfile or pass args in CI
```

### Exercise 6.D.2 — Debug: Flaky Tests

**Scenario:** Tests pass 90% of the time. Occasionally, one test fails.

```python
# BROKEN: Test depends on timing
import time

def test_performance():
    start = time.time()
    result = do_computation()
    elapsed = time.time() - start
    assert elapsed < 0.1  # Fails on slow CI runners!

# FIX: Don't test timing in unit tests. Use benchmarks separately.
def test_computation_result():
    result = do_computation()
    assert result == expected_value


# BROKEN: Test depends on dictionary ordering (Python 3.7+ preserves insertion order, but test is fragile)
def test_response_format():
    response = client.get("/users")
    assert str(response.json()) == "{'id': 1, 'name': 'Alice'}"  # String comparison!

# FIX: Compare values, not string representations
def test_response_format():
    data = client.get("/users").json()
    assert data["id"] == 1
    assert data["name"] == "Alice"


# BROKEN: Test depends on test execution order
class TestDatabase:
    def test_create(self):
        create_user("Alice")
    
    def test_read(self):
        user = get_user("Alice")  # Depends on test_create running first!
        assert user is not None

# FIX: Each test sets up its own state
class TestDatabase:
    def test_create(self):
        create_user("Alice")
        assert get_user("Alice") is not None
    
    def test_read(self):
        create_user("Bob")  # Own setup
        user = get_user("Bob")
        assert user is not None
```

### Exercise 6.D.3 — Debug: Docker Build Fails in CI but Works Locally

```bash
# Cause 1: .dockerignore is different (or missing)
# Local build has .dockerignore, CI checkout doesn't
# Fix: Commit .dockerignore to git

# Cause 2: Docker layer cache is stale locally
# Local: cached old base image. CI: pulls fresh base image with breaking change
docker build --no-cache -t test .  # Test locally without cache

# Cause 3: Build context too large
# CI runner has limited disk
docker build . 2>&1 | head -5
# "Sending build context to Docker daemon  2.5GB"  ← TOO LARGE
# Fix: .dockerignore

# Cause 4: Multi-stage COPY --from fails
# The stage name is case-sensitive and must match exactly
# COPY --from=Builder  ← wrong (capital B)
# COPY --from=builder  ← correct
```

### Exercise 6.D.4 — Debug: Secrets Exposure

**Scenario:** A developer accidentally committed a secret to the repo.

```bash
# SCENARIO: .env file with secrets was committed
# .env contains: DATABASE_URL=postgresql://admin:password@prod-db:5432/app

# Step 1: Remove from current state
git rm .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env, add to .gitignore"

# Step 2: The secret is STILL in git history!
git log --all --oneline -- .env
# You can see the file in old commits

# Step 3: Rotate the secret IMMEDIATELY
# Change the database password in production
# The exposed password is compromised regardless of what you do in git

# Step 4: (Optional) Rewrite git history to remove the file
# WARNING: This rewrites commit hashes — coordinate with team
# git filter-repo --path .env --invert-paths

# PREVENTION:
# 1. Use .env.example (no real values) committed to git
# 2. Use CI/CD secrets management (GitHub Secrets, Vault, etc.)
# 3. Use pre-commit hooks to scan for secrets
```

### Exercise 6.D.5 — Debug: Pipeline Takes 20 Minutes

**Scenario:** CI builds take 20 minutes. The team stops running CI.

```yaml
# BEFORE: 20 minutes
# - Installing Python from source: 5 min
# - Installing all deps without cache: 8 min
# - Docker build without cache: 5 min
# - Tests: 2 min

# AFTER: 3 minutes
# 1. Use setup-uv action with cache
# 2. Use Docker layer cache
# 3. Run lint and test in parallel (separate jobs)
# 4. Only build Docker on main branch

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      - run: uv python install 3.11
      - run: uv sync --frozen --dev
      - run: uv run ruff check src/ tests/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      - run: uv python install 3.11
      - run: uv sync --frozen --dev
      - run: uv run pytest tests/ -v

  docker:
    runs-on: ubuntu-latest
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'  # Skip Docker on PRs
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Complete CI/CD Pipeline for `practical-production-service`

**Task:** Set up a complete CI/CD pipeline that covers the entire lifecycle: push → test → build → deploy.

**Complete CI/CD Workflow:**

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ============================================================
  # Job 1: Quality checks (lint + format)
  # ============================================================
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - run: uv python install 3.11
      - run: uv sync --frozen --dev
      - run: uv lock --check
      - run: uv run ruff check src/ tests/
      - run: uv run ruff format --check src/ tests/

  # ============================================================
  # Job 2: Tests
  # ============================================================
  test:
    name: Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync --frozen --dev
      
      - name: Run tests
        run: uv run pytest tests/ -v --tb=short --junitxml=test-results-${{ matrix.python-version }}.xml

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-py${{ matrix.python-version }}
          path: test-results-*.xml

  # ============================================================
  # Job 3: Docker build (on main branch only)
  # ============================================================
  docker:
    name: Docker Build
    runs-on: ubuntu-latest
    needs: [quality, test]
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to container registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Smoke test built image
        run: |
          docker run -d --name smoke-test -p 8000:8000 ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          sleep 5
          curl -f http://localhost:8000/health
          docker stop smoke-test && docker rm smoke-test

  # ============================================================
  # Job 4: Deploy (on tag push only)
  # ============================================================
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [docker]
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production  # Requires manual approval in GitHub

    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            set -euo pipefail
            
            IMAGE="${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}"
            
            echo "Deploying $IMAGE..."
            docker pull "$IMAGE"
            
            # Graceful shutdown
            docker stop production-service 2>/dev/null || true
            docker rm production-service 2>/dev/null || true
            
            # Start new version
            docker run -d \
              --name production-service \
              --restart unless-stopped \
              -p 8000:8000 \
              -e APP_VERSION=${{ github.ref_name }} \
              "$IMAGE"
            
            # Health check
            for i in $(seq 1 30); do
              if curl -sf http://localhost:8000/health > /dev/null; then
                echo "✓ Deployment successful"
                exit 0
              fi
              sleep 1
            done
            
            echo "✗ Deployment failed: health check timeout"
            docker logs production-service
            exit 1
```

**Create a deploy script for manual deployments:**

```bash
# scripts/deploy.sh
#!/bin/bash
set -euo pipefail

VERSION="${1:?Usage: $0 <version>}"
IMAGE="ghcr.io/your-org/practical-production-service:${VERSION}"

echo "=== Deploying $IMAGE ==="

docker pull "$IMAGE"
docker stop production-service 2>/dev/null || true
docker rm production-service 2>/dev/null || true

docker run -d \
  --name production-service \
  --restart unless-stopped \
  -p 8000:8000 \
  "$IMAGE"

echo "Waiting for health check..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:8000/health > /dev/null; then
        echo "✓ Deployed $VERSION successfully"
        exit 0
    fi
    sleep 1
done

echo "✗ Deployment failed"
docker logs production-service
exit 1
```

**Acceptance Criteria:**
- [ ] CI runs on every push and PR
- [ ] Lint and test jobs run in parallel
- [ ] Tests run on multiple Python versions (matrix)
- [ ] Docker image is built only on main branch
- [ ] Docker image is tagged with git SHA and version
- [ ] Smoke test verifies the image works after build
- [ ] Deploy only happens on version tags (e.g., `v0.1.0`)
- [ ] Deploy includes health check verification
- [ ] Failed lint/test blocks merge (via branch protection)
- [ ] `scripts/run_ci_local.sh` reproduces CI checks locally
- [ ] No secrets in code — all secrets via GitHub Secrets

---

## Key Takeaways

1. **CI is non-negotiable.** Every push should trigger automated tests. No exceptions.
2. **Run CI locally before pushing.** `scripts/run_ci_local.sh` saves round-trip time.
3. **Lockfile verification (`uv lock --check`)** catches forgotten dependency updates.
4. **Cache everything**: uv packages, Docker layers, pip downloads. Speed matters.
5. **Docker smoke test in CI** catches "builds but doesn't run" problems early.
6. **Tag-based releases** give you reproducible deployments (`v0.1.0` always deploys the same code).
7. **Never store secrets in code.** Use CI/CD secret management.

---

*Next: [Section 7 — Monitoring & Observability](07-monitoring-observability.md)*
