# SECTION 0 — UV + PYTHON ENVIRONMENT THEORY & LAB

---

## PART A — CONCEPT EXPLANATION

### What is `uv`?

`uv` is an extremely fast Python package and project manager written in Rust by the Astral team (creators of `ruff`). It replaces `pip`, `pip-tools`, `virtualenv`, `pipenv`, and `poetry` — with a single, unified tool that is **10–100× faster** than pip.

Think of `uv` the way `cargo` works for Rust: it manages your project metadata, dependencies, virtual environment, lockfile, and builds — all in one command.

### Why `uv` Instead of `pip`?

| Problem with `pip` | How `uv` fixes it |
|---|---|
| `pip` does not resolve dependencies deterministically | `uv` uses a SAT-solver for deterministic resolution |
| `pip freeze` captures the world, not your intent | `uv` separates declared deps (pyproject.toml) from resolved deps (uv.lock) |
| `pip` has no built-in lockfile | `uv lock` generates a cross-platform lockfile |
| Virtual env creation is a separate tool | `uv venv` creates venvs; `uv sync` auto-creates one if missing |
| Reinstalling from scratch is slow | `uv` caches aggressively — rebuilds take seconds |
| Reproducibility is manual | `uv sync --frozen` guarantees the exact same packages everywhere |

**Mental model:** `pip` is a hammer. `uv` is a build system. You wouldn't build a house with just a hammer.

### What is `pyproject.toml`?

`pyproject.toml` is the **single source of truth** for your Python project's metadata and dependencies. It replaces `setup.py`, `setup.cfg`, `requirements.txt`, and `MANIFEST.in`.

```toml
[project]
name = "appcore"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104",
    "uvicorn>=0.24",
]

[project.scripts]
appcore-serve = "appcore.cli:serve"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Key sections:
- **`[project]`** — your package name, version, dependencies
- **`[project.scripts]`** — CLI entrypoints (installable commands)
- **`[build-system]`** — how to build your package (hatchling, setuptools, etc.)

### What is Dependency Resolution?

When you say "I need FastAPI and some-other-lib", both may depend on `pydantic` — but different versions. **Dependency resolution** finds a set of versions that satisfies *all* constraints simultaneously, or tells you it's impossible.

```
Your project
├── fastapi >=0.104  → needs pydantic >=2.0
└── old-lib ==1.0    → needs pydantic <2.0
```

This is a **conflict**. pip would silently install one version and break the other. `uv` would tell you immediately.

### What is a Lockfile?

A **lockfile** (`uv.lock`) records the *exact* resolved versions of every dependency, including transitive ones. It answers: "When I ran `uv lock`, what exact versions were chosen?"

```
pyproject.toml  →  "I need fastapi>=0.104"       (intent)
uv.lock         →  "fastapi==0.115.6, ..."       (reality)
```

**Why it matters:**
- Without a lockfile, `uv add fastapi` today might install 0.115.6, but tomorrow 0.116.0 — which might have breaking changes.
- The lockfile ensures that every developer, CI runner, and Docker build gets the **exact same packages**.
- `uv sync --frozen` installs from the lockfile without re-resolving.

### Why Reproducibility Matters

"Works on my machine" is the #1 cause of production failures in Python. Here's how it happens:

1. Developer A runs `pip install fastapi` → gets 0.115.6
2. Developer B runs `pip install fastapi` two weeks later → gets 0.116.0 (has a subtle behavior change)
3. CI runs `pip install fastapi` → gets 0.116.1
4. Production Docker build → gets 0.115.5 (cached layer from a month ago)

Four different environments. Four different behaviors. **Reproducibility** means: given the same source code, you get the **exact same environment** every time.

`uv` achieves this through:
- `pyproject.toml` — declares intent
- `uv.lock` — locks exact versions
- `uv sync --frozen` — installs exactly what's locked, fails if lock is stale

### How Virtual Environments Isolate Packages

A virtual environment is a **directory** that contains:
- A copy/symlink of the Python interpreter
- A `site-packages/` directory for installed packages
- Activation scripts that modify `$PATH` so `python` points to this copy

```
.venv/
├── bin/
│   ├── python → /usr/bin/python3.11
│   ├── activate
│   └── uvicorn
├── lib/
│   └── python3.11/
│       └── site-packages/
│           ├── fastapi/
│           └── uvicorn/
└── pyvenv.cfg
```

**Without a venv:** all packages go into the system Python's `site-packages`. Project A needs `pydantic==1.10`, Project B needs `pydantic==2.5` — impossible to have both.

**With a venv:** each project has its own `site-packages`. Complete isolation.

### How Environment Drift Happens

**Environment drift** = your development environment gradually diverges from production.

Common causes:
1. **Ad-hoc installs**: Running `pip install debugpy` in dev but not recording it
2. **Stale lockfiles**: Not running `uv lock` after changing `pyproject.toml`
3. **System dependency changes**: OS updates upgrade `libssl` → breaks cryptography package
4. **Python version mismatch**: Dev uses 3.12, production uses 3.11
5. **Cached Docker layers**: Dockerfile caches old packages unless layer is invalidated

**Prevention:**
- Always add deps via `uv add`, never `pip install`
- Commit `uv.lock` to git
- Use `uv sync --frozen` in CI and Docker
- Pin Python version in `pyproject.toml` via `requires-python`

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "I can just `pip freeze > requirements.txt`" | This captures transitive deps with no intent separation — impossible to maintain |
| "Virtual environments are optional" | They're mandatory for any serious work. Without them you'll corrupt other projects |
| "Lockfiles slow me down" | They save you hours of debugging mysterious failures later |
| "`uv` is just faster pip" | `uv` is a project manager — it handles resolution, locking, building, and publishing |
| "I'll set up the environment later" | Environment setup is step 1. Everything else depends on it |

---

## PART B — BEGINNER PRACTICE

### Exercise 0.B.1 — Install uv

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

**Expected output:**
```
uv 0.5.x (or newer)
```

**What happened:** `uv` is a single binary. The install script downloads it to `~/.local/bin/` (or `~/.cargo/bin/`) and adds it to your PATH.

### Exercise 0.B.2 — Create a New Project

```bash
# Create the project that will evolve through the entire bootcamp
uv init practical-production-service
cd practical-production-service
```

**Expected output:**
```
Initialized project `practical-production-service`
```

**Inspect what was created:**
```bash
ls -la
cat pyproject.toml
```

You should see a `pyproject.toml` with default metadata and a `hello.py` sample file.

### Exercise 0.B.3 — Create a Virtual Environment

```bash
# Create a venv using uv
uv venv

# Inspect it
ls -la .venv/
ls .venv/bin/
```

**Expected output:** A `.venv/` directory with `bin/python`, `bin/activate`, etc.

**Verify it's isolated:**
```bash
# Check which Python the venv uses
.venv/bin/python --version

# Compare with system Python
which python3
python3 --version
```

### Exercise 0.B.4 — Set Up src-layout

```bash
# Remove the default hello.py
rm hello.py

# Create src-layout structure
mkdir -p src/appcore/api src/appcore/config src/appcore/monitoring
touch src/appcore/__init__.py
touch src/appcore/cli.py
touch src/appcore/logic.py
touch src/appcore/api/__init__.py
touch src/appcore/api/app.py
touch src/appcore/api/routes.py
touch src/appcore/config/__init__.py
touch src/appcore/config/settings.py
touch src/appcore/monitoring/__init__.py
touch src/appcore/monitoring/metrics.py
```

**Verify the structure:**
```bash
find src/ -type f | sort
```

**Expected:**
```
src/appcore/__init__.py
src/appcore/api/__init__.py
src/appcore/api/app.py
src/appcore/api/routes.py
src/appcore/cli.py
src/appcore/config/__init__.py
src/appcore/config/settings.py
src/appcore/logic.py
src/appcore/monitoring/__init__.py
src/appcore/monitoring/metrics.py
```

### Exercise 0.B.5 — Configure pyproject.toml

Edit `pyproject.toml` to match the project specification:

```toml
[project]
name = "appcore"
version = "0.1.0"
description = "Production-ready service for the bootcamp"
requires-python = ">=3.11"
dependencies = []

[project.scripts]
appcore-serve = "appcore.cli:serve"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/appcore"]
```

**Why `[tool.hatch.build.targets.wheel]`?** Because we're using src-layout, we need to tell the build system where to find the package.

### Exercise 0.B.6 — Add Dependencies

```bash
# Add project dependencies one at a time
uv add fastapi
uv add uvicorn
uv add pydantic
uv add prometheus-client

# Check what happened
cat pyproject.toml
```

**Expected:** The `[project] dependencies` section now lists all four packages.

```bash
# Inspect the lockfile
head -50 uv.lock
```

**Observe:** The lockfile contains the exact resolved versions of FastAPI, uvicorn, pydantic, *and all their transitive dependencies*.

### Exercise 0.B.7 — Install the Project in Editable Mode

```bash
# Sync the environment (installs all deps + your package)
uv sync

# Verify your package is installed
uv run python -c "import appcore; print('appcore imported successfully')"
```

**Expected:** No import error. Your package is available because `uv sync` installed it in editable mode.

### Exercise 0.B.8 — Add a Dev Dependency

```bash
# Add pytest as a development dependency
uv add --dev pytest
uv add --dev httpx  # needed for FastAPI test client

# Check pyproject.toml
grep -A 5 "dev" pyproject.toml
```

**Expected:** Dev dependencies appear in `[dependency-groups]` section, separate from production deps.

### Exercise 0.B.9 — Write and Run a Minimal Test

```bash
mkdir -p tests
```

Create `tests/test_smoke.py`:
```python
def test_import():
    import appcore
    assert appcore is not None

def test_python_version():
    import sys
    assert sys.version_info >= (3, 11)
```

```bash
uv run pytest tests/ -v
```

**Expected:** Two passing tests.

### Exercise 0.B.10 — Understand `uv run`

```bash
# These are equivalent:
uv run python -c "import fastapi; print(fastapi.__version__)"
uv run pytest tests/ -v
uv run uvicorn --version

# This would FAIL without uv run (unless venv is activated):
python -c "import fastapi; print(fastapi.__version__)"
```

**Why?** `uv run` automatically locates the `.venv`, activates it, and runs the command inside it. You never need to manually `source .venv/bin/activate`.

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 0.C.1 — Simulate Dependency Conflict

```bash
# Try adding a package that conflicts with your current dependencies
# First, check current pydantic version
uv run python -c "import pydantic; print(pydantic.__version__)"

# Now try to add an old package that needs pydantic v1
uv add "pydantic<2"
```

**What to observe:** `uv` will either:
1. Downgrade pydantic and warn you that FastAPI needs pydantic v2 (conflict)
2. Refuse to resolve and show an error

**Read the error carefully.** This is what dependency resolution looks like when it fails.

```bash
# Fix it by removing the constraint
uv remove pydantic
uv add pydantic
```

### Exercise 0.C.2 — Destroy and Rebuild the Environment

```bash
# Delete the entire virtual environment
rm -rf .venv

# Rebuild from lockfile only (frozen = don't re-resolve, just install)
uv sync --frozen

# Verify everything works
uv run python -c "import fastapi; print('OK')"
uv run pytest tests/ -v
```

**What this proves:** The lockfile contains enough information to perfectly recreate your environment. This is **reproducibility**.

### Exercise 0.C.3 — Audit Your Dependency Tree

```bash
# Show the full dependency tree
uv tree
```

**Study the output.** You'll see:
- Your declared dependencies (fastapi, uvicorn, etc.)
- Their transitive dependencies (starlette, anyio, etc.)
- Exact versions for everything

**Question for yourself:** If starlette has a security vulnerability, how would you know it's in your project?

### Exercise 0.C.4 — Pin Python Version and Validate

```bash
# Check what Python version uv is using
uv run python --version

# Explicitly pin in pyproject.toml
# requires-python = ">=3.11,<3.13"
```

Edit `pyproject.toml` to set `requires-python = ">=3.11,<3.13"`.

```bash
# Re-lock with the constraint
uv lock

# If you had Python 3.13, this would now fail:
# uv sync → error: requires python <3.13
```

### Exercise 0.C.5 — Use Environment Variables with `uv run`

Create a file `src/appcore/config/settings.py`:

```python
import os

def get_settings():
    return {
        "app_name": os.getenv("APP_NAME", "appcore"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "port": int(os.getenv("PORT", "8000")),
    }
```

```bash
# Run with environment variables
APP_NAME=myservice DEBUG=true uv run python -c "
from appcore.config.settings import get_settings
print(get_settings())
"
```

**Expected:**
```
{'app_name': 'myservice', 'debug': True, 'port': 8000}
```

### Exercise 0.C.6 — Export Requirements for Comparison

```bash
# uv can export a pip-compatible requirements file
uv export --format requirements-txt --no-hashes > requirements.exported.txt

# Compare what uv locked vs what pip freeze would show
cat requirements.exported.txt
```

**Why this matters:** Some deployment targets (e.g., legacy systems) only understand `requirements.txt`. `uv export` bridges the gap without abandoning proper dependency management.

### Exercise 0.C.7 — Test Lock Staleness

```bash
# Manually edit pyproject.toml and add a new dependency
# Add: "httpx>=0.25" to [project] dependencies

# Now try to sync with --frozen
uv sync --frozen
```

**Expected error:** `uv` refuses because the lockfile doesn't match `pyproject.toml`. The lock is "stale."

```bash
# Fix: re-lock first, then sync
uv lock
uv sync
```

**Production lesson:** CI should run `uv sync --frozen`. If it fails, someone forgot to commit an updated `uv.lock`.

---

## PART D — ADVANCED DEBUG LAB

### Exercise 0.D.1 — Debug: "Module Not Found" After Install

**Scenario:** You've run `uv sync`, but `import appcore` fails.

**Intentionally break it:**
```bash
# Remove the hatch build config from pyproject.toml
# Delete the [tool.hatch.build.targets.wheel] section
# Then re-sync
uv sync
uv run python -c "import appcore"
```

**Diagnosis steps:**
```bash
# 1. Check if the package is installed
uv run pip list | grep appcore

# 2. Check the sys.path
uv run python -c "import sys; print('\n'.join(sys.path))"

# 3. Check if the src directory is in the path
ls .venv/lib/python*/site-packages/ | grep appcore
```

**Root cause:** Without `[tool.hatch.build.targets.wheel] packages = ["src/appcore"]`, hatchling doesn't know where your code is.

**Fix:** Restore the `[tool.hatch.build.targets.wheel]` section and re-run `uv sync`.

### Exercise 0.D.2 — Debug: Conflicting Transitive Dependencies

**Scenario:** Two packages need incompatible versions of a shared dependency.

```bash
# Create a test project
cd /tmp
uv init conflict-test
cd conflict-test
uv add fastapi

# Now add a package with an old pydantic pin
# (simulate by manually editing pyproject.toml)
```

Add this to `pyproject.toml` dependencies:
```toml
dependencies = [
    "fastapi>=0.104",
    "pydantic>=1.0,<2.0",
]
```

```bash
uv lock
```

**Study the error output.** Learn to read resolution failures:
- Which packages conflict?
- What versions does each require?
- What is the resolution impossible set?

```bash
# Clean up
cd -
rm -rf /tmp/conflict-test
```

### Exercise 0.D.3 — Debug: Stale .venv with Wrong Python

**Scenario:** The `.venv` was created with Python 3.10 but your project requires >=3.11.

```bash
# Simulate by checking the venv's Python
cat .venv/pyvenv.cfg
```

**What to look for:**
- `version = 3.x.y` — does this match `requires-python`?
- `home = /path/to/python` — is this the expected Python?

**If mismatched:**
```bash
rm -rf .venv
uv venv --python 3.11
uv sync
```

### Exercise 0.D.4 — Debug: CI Fails but Local Works

**Scenario:** `uv sync --frozen` passes locally but fails in CI.

**Common causes:**
1. `uv.lock` not committed to git
2. `uv.lock` is stale (pyproject.toml changed but lock wasn't regenerated)
3. Different Python version in CI
4. Missing system dependencies (e.g., `libffi-dev` for `cffi`)

**Diagnostic checklist:**
```bash
# Is uv.lock committed?
git ls-files uv.lock

# Is it up to date?
uv lock --check  # exits non-zero if lock is stale

# What Python does CI use?
uv run python --version

# Are system deps present?
dpkg -l | grep libffi  # Debian/Ubuntu
```

### Exercise 0.D.5 — Debug: Docker Build Fails on `uv sync`

**Scenario:** Dockerfile uses `uv sync` but fails with "No pyproject.toml found".

**Broken Dockerfile:**
```dockerfile
FROM python:3.11-slim
RUN pip install uv
WORKDIR /app
RUN uv sync
COPY . .
CMD ["uv", "run", "uvicorn", "appcore.api.app:app"]
```

**What's wrong?** `COPY . .` happens *after* `RUN uv sync`. The `pyproject.toml` isn't in the container yet when `uv sync` runs.

**Fixed Dockerfile:**
```dockerfile
FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "uvicorn", "appcore.api.app:app", "--host", "0.0.0.0"]
```

**Key lesson:** In Docker, copy dependency files first, install, then copy source code. This maximizes layer caching.

---

## PART E — PRODUCTION SIMULATION

### Scenario: New Developer Onboarding

**Situation:** A new team member clones the repository on a fresh machine. They need to have the exact same environment running within 5 minutes.

**Acceptance Criteria:**

1. Clone the repo
2. Run a single command to set up the environment
3. All tests pass
4. The service starts and responds on `/health`

**Steps to validate:**

```bash
# Simulate fresh clone
cd /tmp
git clone <your-repo-url> fresh-clone
cd fresh-clone

# One command setup
uv sync

# Tests pass
uv run pytest tests/ -v

# Service starts (if you've built the API already)
uv run uvicorn appcore.api.app:app --host 0.0.0.0 --port 8000 &
curl http://localhost:8000/health
kill %1
```

**Validation checklist:**
- [ ] `uv sync` completes without errors
- [ ] No manual `pip install` needed
- [ ] No `source .venv/bin/activate` needed
- [ ] Python version matches `requires-python`
- [ ] All tests pass on first try
- [ ] `uv.lock` exists and is not stale (`uv lock --check` passes)

### Scenario: Reproducible CI Build

**Write a GitHub Actions step that:**

```yaml
- name: Set up uv
  uses: astral-sh/setup-uv@v4

- name: Set up Python
  run: uv python install 3.11

- name: Install dependencies
  run: uv sync --frozen --dev

- name: Run tests
  run: uv run pytest tests/ -v

- name: Verify lock is fresh
  run: uv lock --check
```

**Why `--frozen`?** It guarantees CI uses the exact lockfile from version control. If someone changed `pyproject.toml` without updating the lock, CI fails loudly — which is exactly what you want.

---

## Key Takeaways

1. **`uv` replaces the entire pip + virtualenv + pip-tools stack** with a single fast tool
2. **`pyproject.toml` is intent**, `uv.lock` is reality — both are committed to git
3. **`uv sync --frozen`** is the most important command for reproducibility
4. **Never run `pip install` directly** — always go through `uv add` or `uv sync`
5. **Environment drift is the root cause** of most "works on my machine" bugs
6. **Delete and rebuild `.venv` freely** — the lockfile ensures you can always recreate it

---

*Next: [Section 1 — Linux Fundamentals](01-linux-fundamentals.md)*
