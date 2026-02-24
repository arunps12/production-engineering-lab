# SECTION 9 — DOCKER THEORY & LAB

---

## PART A — CONCEPT EXPLANATION

### What is a Container?

A **container** is a lightweight, isolated environment for running a process. It shares the host OS kernel but has its own:
- Filesystem (via overlay filesystem)
- Process table (via PID namespace)
- Network stack (via network namespace)
- User IDs (via user namespace)

```
                       Virtual Machine              Container
                     ┌──────────────────┐      ┌──────────────────┐
                     │    Your App      │      │    Your App      │
                     │    Libraries     │      │    Libraries     │
                     │    Guest OS      │      │                  │
                     │    Hypervisor    │      │  Container Runtime│
                     │    Host OS       │      │    Host OS       │
                     │    Hardware      │      │    Hardware      │
                     └──────────────────┘      └──────────────────┘
                     ~1GB+ overhead             ~10MB overhead
                     Boots in minutes           Starts in milliseconds
```

**Mental model:** A container is like a chroot on steroids. It's not a VM — there's no guest OS, no hypervisor. It's just a regular process with heavy isolation walls around it.

**Why containers exist:** "Works on my machine" → because your machine has Python 3.12, libssl-1.1, and Ubuntu 22.04. Production has Python 3.11, libssl-3, and Alpine. A container bundles the **exact** environment, so it runs identically everywhere.

### What is a Layer?

A Docker image is built from **layers** — each instruction in a Dockerfile creates one layer. Layers are:
- **Read-only** — once built, they never change
- **Cached** — if the input hasn't changed, Docker reuses the cached layer
- **Shared** — multiple images can share the same base layers

```
Layer 5: COPY . .              ← Your source code (changes often)
Layer 4: RUN uv sync           ← Dependencies (changes sometimes)
Layer 3: COPY pyproject.toml . ← Dependency specification (changes rarely)
Layer 2: RUN apt-get install   ← System packages (changes rarely)
Layer 1: FROM python:3.11-slim ← Base image (changes almost never)
```

**Why layer order matters:** Docker builds top-down. When it finds a layer that changed, it rebuilds all layers **above** it. If you put `COPY . .` (changing source code) before `RUN uv sync` (installing deps), every code change reinstalls all dependencies.

**Optimal order:** Things that change **least** go at the **bottom**. Things that change **most** go at the **top**.

### What is Image vs Container?

| Concept | Analogy | Description |
|---|---|---|
| **Image** | Blueprint / Class | A read-only template. Contains filesystem, env vars, default CMD |
| **Container** | Instance / Object | A running instance of an image. Has state, runs a process |

```bash
# Image = blueprint
docker build -t myapp .

# Container = running instance
docker run myapp        # Create + start a container from the image
docker run myapp        # Create another container (independent!)
docker run myapp        # A third one (all from the same image)
```

You can:
- Have one image and 100 containers
- Stop/restart containers without rebuilding the image
- Export an image to a `.tar` file and import it on another machine

### What is Port Mapping?

Containers have their own network stack. A process listening on port 8000 **inside** a container is not accessible from the host unless you explicitly map the port.

```
Without port mapping:
  Host:      curl http://localhost:8000 → Connection refused
  Container: curl http://localhost:8000 → 200 OK

With -p 8000:8000:
  Host:      curl http://localhost:8000 → (forwarded to container:8000) → 200 OK
  Container: curl http://localhost:8000 → 200 OK
```

```bash
# -p HOST_PORT:CONTAINER_PORT
docker run -p 8000:8000 myapp      # Host 8000 → Container 8000
docker run -p 9000:8000 myapp      # Host 9000 → Container 8000
docker run -p 8000:8000 -p 9090:9090 myapp  # Map multiple ports
```

**Critical requirement:** The app inside the container MUST bind to `0.0.0.0`, not `127.0.0.1`. If it binds to `127.0.0.1`, port mapping won't work because `127.0.0.1` inside the container refers only to the container's own loopback.

### What is a Multi-Stage Build?

A **multi-stage build** uses multiple `FROM` statements to create intermediate images, then copies only the needed artifacts to the final image.

**Problem without multi-stage:**
```dockerfile
FROM python:3.11
RUN apt-get install -y gcc build-essential  # 500MB of build tools
COPY . .
RUN pip install .
CMD ["uvicorn", "app:app"]
# Final image: ~1.2GB (includes gcc, headers, source code, caches)
```

**With multi-stage:**
```dockerfile
# Stage 1: Build
FROM python:3.11 AS builder
RUN apt-get install -y gcc
COPY . .
RUN pip install --target=/install .

# Stage 2: Runtime (only what's needed)
FROM python:3.11-slim
COPY --from=builder /install /usr/local/lib/python3.11/site-packages
COPY src/ /app/src/
CMD ["uvicorn", "app:app"]
# Final image: ~200MB (no gcc, no build tools, no source caches)
```

**Why it matters:** Smaller images = faster pulls, less disk, smaller attack surface (no gcc in production).

### Why Docker Builds Become Large

Common causes of bloated images:

| Cause | Size Impact | Fix |
|---|---|---|
| Using `python:3.11` instead of `python:3.11-slim` | +600MB | Use `-slim` variant |
| Installing build tools and not removing them | +200MB | Multi-stage build |
| `COPY . .` copies `.git/`, `.venv/`, `__pycache__/` | +100MB+ | Use `.dockerignore` |
| pip cache not cleared | +100MB | `pip install --no-cache-dir` or use uv |
| Multiple `RUN apt-get install` commands | Extra layers | Combine into one `RUN` |
| Not combining `apt-get update && install` | Stale package lists | Always combine them |

**Essential `.dockerignore`:**
```
.git
.venv
__pycache__
*.pyc
.pytest_cache
.mypy_cache
node_modules
*.egg-info
dist
build
```

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "Docker is a virtual machine" | Containers share the host kernel. No hypervisor, no guest OS |
| "My image is small because the Dockerfile is short" | Image size depends on base image and installed packages, not Dockerfile length |
| "I need to rebuild everything when code changes" | Proper layer ordering means only the changed layer and above are rebuilt |
| "`EXPOSE 8000` opens the port" | `EXPOSE` is documentation only. You need `-p 8000:8000` at runtime |
| "Docker volumes persist automatically" | Containers are ephemeral. Data in the container filesystem is lost when the container is removed |
| "`docker run` reuses the last container" | `docker run` ALWAYS creates a new container. Use `docker start` to restart an existing one |

---

## PART B — BEGINNER PRACTICE

### Exercise 5.B.1 — Verify Docker Installation

```bash
# Check Docker is installed and running
docker --version
docker info | head -10

# Run a test container
docker run --rm hello-world

# List images
docker images

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

### Exercise 5.B.2 — Run a Container Interactively

```bash
# Run Ubuntu interactively
docker run -it --rm ubuntu:22.04 bash

# Inside the container:
whoami          # root
cat /etc/os-release
ls /
ps aux          # very few processes
exit

# The container is gone (--rm flag)
docker ps -a | grep ubuntu
```

### Exercise 5.B.3 — Build Your First Dockerfile

Create in your `practical-production-service` project:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev deps, no project itself yet)
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY src/ src/

# Install the project itself
RUN uv sync --frozen --no-dev

# Expose port (documentation only)
EXPOSE 8000

# Run the server
CMD ["uv", "run", "uvicorn", "appcore.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build the image
docker build -t production-service .

# Check image size
docker images production-service
```

### Exercise 5.B.4 — Run Your Container

```bash
# Run the container
docker run -d --name myservice -p 8000:8000 production-service

# Check it's running
docker ps

# Test the API
curl http://localhost:8000/health | python3 -m json.tool
curl http://localhost:8000/version | python3 -m json.tool
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}'

# View logs
docker logs myservice

# Follow logs in real-time
docker logs -f myservice &
curl http://localhost:8000/health
kill %1

# Stop the container
docker stop myservice

# Remove the container
docker rm myservice
```

### Exercise 5.B.5 — Understand `.dockerignore`

```bash
# Create .dockerignore
cat > .dockerignore <<'EOF'
.git
.venv
__pycache__
*.pyc
.pytest_cache
.mypy_cache
*.egg-info
dist
build
.env
EOF

# Rebuild (should be faster with fewer files to copy)
docker build -t production-service .
```

### Exercise 5.B.6 — Inspect a Docker Image

```bash
# Show image layers
docker history production-service

# Detailed inspection
docker inspect production-service | python3 -m json.tool | head -50

# Check image size breakdown
docker history --no-trunc production-service | awk '{print $1, $NF}'

# Get into a running container for debugging
docker run -it --rm production-service bash
ls /app/
ls /app/src/
exit
```

### Exercise 5.B.7 — Environment Variables in Docker

```bash
# Pass environment variables
docker run -d --name myservice \
  -p 8000:8000 \
  -e APP_NAME=production-service \
  -e DEBUG=true \
  -e LOG_LEVEL=DEBUG \
  production-service

# Verify inside the container
docker exec myservice env | grep -E "APP_NAME|DEBUG|LOG_LEVEL"

# Test that settings picked up the env vars
curl http://localhost:8000/version | python3 -m json.tool

docker stop myservice && docker rm myservice
```

### Exercise 5.B.8 — Docker Volumes for Persistent Data

```bash
# Create a volume
docker volume create service-data

# Run with volume mounted
docker run -d --name myservice \
  -p 8000:8000 \
  -v service-data:/app/data \
  production-service

# Write data inside the container
docker exec myservice sh -c "echo 'persistent data' > /app/data/test.txt"

# Stop and remove the container
docker stop myservice && docker rm myservice

# Start a NEW container with the same volume
docker run -d --name myservice2 \
  -p 8000:8000 \
  -v service-data:/app/data \
  production-service

# Data persists!
docker exec myservice2 cat /app/data/test.txt

docker stop myservice2 && docker rm myservice2
docker volume rm service-data
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 5.C.1 — Multi-Stage Build

```dockerfile
# Dockerfile.multistage
# Stage 1: Build environment
FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ src/
RUN uv sync --frozen --no-dev

# Stage 2: Runtime (minimal)
FROM python:3.11-slim AS runtime

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

# Copy the entire virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
COPY --from=builder /app/uv.lock /app/uv.lock
COPY src/ src/

# Set PATH to use venv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "appcore.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build both versions
docker build -t service-standard -f Dockerfile .
docker build -t service-multistage -f Dockerfile.multistage .

# Compare sizes
docker images | grep service-
# Multistage should be smaller
```

### Exercise 5.C.2 — Docker Compose

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_NAME=production-service
      - DEBUG=false
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

```bash
# Start with docker-compose
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Test
curl http://localhost:8000/health

# Stop
docker compose down
```

### Exercise 5.C.3 — Layer Caching Experiment

```bash
# Build 1: Clean build (all layers)
docker build --no-cache -t service-test . 2>&1 | tail -5
# Note the total build time

# Build 2: No changes (all cached)
docker build -t service-test . 2>&1 | tail -5
# Should say "CACHED" for every layer

# Build 3: Change source code only
echo "# comment" >> src/appcore/__init__.py
docker build -t service-test . 2>&1 | tail -10
# Only the COPY src/ and CMD layers should rebuild
# Dependencies (uv sync) should be CACHED

# Revert
git checkout src/appcore/__init__.py 2>/dev/null
```

### Exercise 5.C.4 — Docker Networking

```bash
# Create a custom network
docker network create app-network

# Start two containers on the same network
docker run -d --name api --network app-network -p 8000:8000 production-service
docker run -d --name debug --network app-network python:3.11-slim sleep 3600

# From the debug container, reach the api container BY NAME
docker exec debug sh -c "apt-get update -qq && apt-get install -y -qq curl > /dev/null 2>&1"
docker exec debug curl http://api:8000/health

# Docker DNS resolves "api" to the container's IP on app-network
docker exec debug nslookup api 2>/dev/null || docker exec debug getent hosts api

# Clean up
docker stop api debug
docker rm api debug
docker network rm app-network
```

**Key learning:** On a custom Docker network, containers can reach each other by **container name** (Docker's built-in DNS). This is how multi-service apps communicate.

### Exercise 5.C.5 — Health Checks

```bash
# Run with health check
docker run -d --name health-test \
  -p 8000:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=3 \
  production-service

# Watch health status
watch -n 2 'docker ps --format "table {{.Names}}\t{{.Status}}"'

# After ~30 seconds, status should show "(healthy)"
# Ctrl+C to stop watch

docker stop health-test && docker rm health-test
```

### Exercise 5.C.6 — Resource Limits

```bash
# Run with memory limit
docker run -d --name limited \
  -p 8000:8000 \
  --memory=256m \
  --cpus=0.5 \
  production-service

# Check resource usage
docker stats limited --no-stream

# Check limits
docker inspect limited --format '{{.HostConfig.Memory}}' | awk '{print $1/1024/1024 "MB"}'

docker stop limited && docker rm limited
```

### Exercise 5.C.7 — Build Arguments

```dockerfile
# Add to Dockerfile (or create Dockerfile.args)
# ARG APP_VERSION=0.1.0
# ENV APP_VERSION=${APP_VERSION}
```

```bash
# Build with custom version
docker build --build-arg APP_VERSION=1.2.3 -t service-v1.2.3 .

# Verify
docker run --rm service-v1.2.3 env | grep APP_VERSION
```

### Exercise 5.C.8 — Docker Exec for Debugging

```bash
docker run -d --name debug-container -p 8000:8000 production-service

# Execute commands inside the running container

# Check processes
docker exec debug-container ps aux

# Check network
docker exec debug-container ss -tlnp

# Check filesystem
docker exec debug-container ls -la /app/

# Check environment
docker exec debug-container env

# Interactive shell
docker exec -it debug-container bash

# Check Python packages
docker exec debug-container uv run pip list

docker stop debug-container && docker rm debug-container
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 5.D.1 — Debug: Container Exits Immediately

**Scenario:** `docker run myapp` exits with code 1 immediately.

```bash
# Simulate: build an image with a broken CMD
cat > /tmp/Dockerfile.broken <<'EOF'
FROM python:3.11-slim
CMD ["python", "-c", "import nonexistent_module"]
EOF

docker build -t broken-app -f /tmp/Dockerfile.broken /tmp

# Run it
docker run broken-app
# Exits immediately

# Diagnosis step 1: Check exit code
docker run broken-app; echo "Exit code: $?"

# Diagnosis step 2: Check logs
docker run --name crash-test broken-app 2>&1 || true
docker logs crash-test

# Diagnosis step 3: Get into the container to debug
docker run -it --rm broken-app bash
# Now you're inside — try running the command manually:
python -c "import nonexistent_module"  # See the actual error

# Clean up
docker rm crash-test
docker rmi broken-app
rm /tmp/Dockerfile.broken
```

### Exercise 5.D.2 — Debug: Port Mapping Not Working

**Scenario:** `-p 8000:8000` is set but `curl http://localhost:8000` returns "Connection refused."

```bash
# Common cause: app binds to 127.0.0.1 inside the container
cat > /tmp/Dockerfile.portbug <<'EOF'
FROM python:3.11-slim
RUN pip install fastapi uvicorn
COPY <<PYEOF /app/main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
PYEOF
# BUG: binding to 127.0.0.1 instead of 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
WORKDIR /app
EOF

docker build -t portbug -f /tmp/Dockerfile.portbug /tmp
docker run -d --name portbug -p 8000:8000 portbug
sleep 2

# This will fail!
curl http://localhost:8000/health 2>&1 || echo "FAILED: Connection refused"

# Diagnose: check what it's listening on INSIDE the container
docker exec portbug ss -tlnp
# Shows: 127.0.0.1:8000 ← That's the bug!

# Fix: Change --host to 0.0.0.0
docker stop portbug && docker rm portbug
docker rmi portbug
rm /tmp/Dockerfile.portbug
```

### Exercise 5.D.3 — Debug: Image Too Large

```bash
# Check image size
docker images production-service --format "{{.Size}}"

# Analyze layer sizes
docker history production-service

# Find the biggest layers
docker history production-service --format "{{.Size}}\t{{.CreatedBy}}" | sort -rh | head -5

# Common fixes:
# 1. Use -slim base image (saves ~600MB)
# 2. Use .dockerignore (saves copying .git, .venv, etc.)
# 3. Multi-stage build (saves build tools)
# 4. Combine RUN commands (fewer layers)
# 5. Clean apt cache in same RUN:
#    RUN apt-get update && apt-get install -y pkg && rm -rf /var/lib/apt/lists/*
```

### Exercise 5.D.4 — Debug: Container Can't Reach External Service

**Scenario:** Your container needs to call an external API, but `curl` fails with "Could not resolve host."

```bash
docker run -it --rm python:3.11-slim bash -c "
  apt-get update -qq && apt-get install -y -qq dnsutils curl > /dev/null 2>&1
  
  # Check DNS
  cat /etc/resolv.conf
  
  # Test DNS resolution
  nslookup google.com
  
  # Test HTTPS
  curl -s https://httpbin.org/get | head -5
"

# If DNS fails inside container:
# 1. Check Docker daemon DNS config: docker info | grep DNS
# 2. Check host DNS: cat /etc/resolv.conf
# 3. Try with explicit DNS: docker run --dns 8.8.8.8 myapp
```

### Exercise 5.D.5 — Debug: Build Cache Not Working

```bash
# Symptom: every build reinstalls all dependencies even with no changes

# Check if your Dockerfile has COPY . . BEFORE dependency install:
# WRONG:
# COPY . .
# RUN uv sync   ← rebuilds every time because COPY . . includes source changes

# CORRECT:
# COPY pyproject.toml uv.lock ./     ← only dep files
# RUN uv sync --no-install-project   ← cached unless deps change
# COPY src/ src/                     ← source code (changes often)
# RUN uv sync                        ← quick, just installs the project

# Verify caching is working:
docker build -t cache-test . 2>&1 | grep -E "CACHED|RUN"
# Modify source code, rebuild:
echo "" >> src/appcore/__init__.py
docker build -t cache-test . 2>&1 | grep -E "CACHED|RUN"
# uv sync for deps should say CACHED
git checkout src/appcore/__init__.py 2>/dev/null
```

### Exercise 5.D.6 — Debug: Zombie Processes in Container

**Scenario:** Your container slowly accumulates zombie processes because PID 1 doesn't reap children.

```bash
# By default, the CMD process becomes PID 1 in the container
# PID 1 is special: it must reap zombie children

# Solution 1: Use --init flag
docker run --init -d --name with-init production-service
docker exec with-init ps aux
# You'll see "tini" as PID 1, which properly reaps zombies

# Solution 2: Use tini in Dockerfile
# RUN apt-get update && apt-get install -y tini
# ENTRYPOINT ["tini", "--"]
# CMD ["uvicorn", "appcore.api.app:app", "--host", "0.0.0.0"]

docker stop with-init && docker rm with-init
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Containerize `practical-production-service` for Production

**Task:** Create a production-grade Docker setup for your service.

**Requirements:**
1. Multi-stage build for minimal image size
2. Non-root user for security
3. Health check
4. Proper layer caching
5. `.dockerignore` to exclude unnecessary files
6. `docker-compose.yml` for easy deployment

**Production Dockerfile:**

```dockerfile
# Dockerfile
# ============================================================
# Stage 1: Build
# ============================================================
FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies only
RUN uv sync --frozen --no-dev --no-install-project

# Copy source and install the project
COPY src/ src/
RUN uv sync --frozen --no-dev

# ============================================================
# Stage 2: Runtime
# ============================================================
FROM python:3.11-slim AS runtime

# Copy uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install tini for proper PID 1 behavior and curl for health checks
RUN apt-get update && \
    apt-get install -y --no-install-recommends tini curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

WORKDIR /app

# Copy built environment from builder
COPY --from=builder --chown=appuser:appuser /app /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use tini as init process
ENTRYPOINT ["tini", "--"]

# Start the application
CMD ["uv", "run", "uvicorn", "appcore.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

**Production docker-compose.yml:**

```yaml
# docker-compose.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: production-service
    ports:
      - "8000:8000"
    environment:
      - APP_NAME=production-service
      - APP_VERSION=0.1.0
      - DEBUG=false
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
```

**Validation:**

```bash
# Build
docker compose build

# Start
docker compose up -d

# Check health (wait for start_period)
sleep 10
docker compose ps

# Test all endpoints
curl http://localhost:8000/health | python3 -m json.tool
curl http://localhost:8000/version | python3 -m json.tool
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0]}' | python3 -m json.tool

# Check image size
docker images production-service --format "{{.Repository}}:{{.Tag}} → {{.Size}}"

# Check container is running as non-root
docker exec production-service whoami
# Expected: appuser

# View structured logs
docker compose logs --tail 20

# Stop
docker compose down
```

**Acceptance Criteria:**
- [ ] Image builds successfully
- [ ] Image size is under 300MB (slim base + multi-stage)
- [ ] Container runs as non-root user (`appuser`)
- [ ] Health check passes (status: healthy)
- [ ] All API endpoints respond correctly
- [ ] Container auto-restarts on failure (`restart: unless-stopped`)
- [ ] Memory limit is set (512M)
- [ ] `.dockerignore` excludes `.git`, `.venv`, `__pycache__`
- [ ] Dependency layer is cached on source-only changes
- [ ] `docker compose up -d` starts the full service
- [ ] Logs show structured request logging

---

## Key Takeaways

1. **Containers are processes, not VMs.** They're fast because they share the host kernel.
2. **Layer order is everything.** Dependencies first, source code last = fast rebuilds.
3. **Always bind to `0.0.0.0` inside containers.** `127.0.0.1` won't work with port mapping.
4. **Use multi-stage builds** to keep production images small.
5. **Run as non-root** in production. It's a security best practice.
6. **Use `.dockerignore`** to avoid copying unnecessary files into the image.
7. **Health checks** let Docker (and orchestrators) know if your service is alive.

---

*Next: [Section 10 — Docker Debug Labs](10-docker-debug-labs.md)*
