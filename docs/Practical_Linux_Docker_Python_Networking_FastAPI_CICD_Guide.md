# Practical Linux, Docker, Python, Networking, REST & CI/CD

## Implementation Specification (Learn by Building)

Author: Arun\
Goal: Become Production-Ready Backend / ML Systems Engineer\
Mode: Execution-Based Learning

------------------------------------------------------------------------

# OBJECTIVE

By completing this guide, you will be able to:

-   Operate confidently in Linux environments (local, HPC, cloud)
-   Package Python projects professionally (src-layout, CLI)
-   Build REST APIs correctly using FastAPI
-   Understand networking deeply enough to debug production issues
-   Containerize systems with Docker
-   Implement CI/CD pipelines
-   Deploy services to a remote server
-   Monitor and version production systems

You will build ONE evolving project:

    practical-production-service/

Every phase upgrades the same system.

------------------------------------------------------------------------

# FINAL TARGET STRUCTURE

    practical-production-service/
    │
    ├── src/
    │   └── appcore/
    │       ├── __init__.py
    │       ├── cli.py
    │       ├── logic.py
    │       ├── api/
    │       │   ├── app.py
    │       │   └── routes.py
    │       ├── config/
    │       │   └── settings.py
    │       └── monitoring/
    │           └── metrics.py
    │
    ├── configs/
    │   └── config.yaml
    │
    ├── tests/
    ├── scripts/
    │   ├── run_local.sh
    │   └── deploy.sh
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .github/workflows/ci.yml
    ├── pyproject.toml
    └── README.md

Everything below must be implemented.

------------------------------------------------------------------------

# PHASE 0 --- LINUX FOUNDATION

## Required Skills

Master:

    ls, cd, pwd, mkdir, rm -rf, mv, cp -r
    grep, find, chmod, chown
    ps, top, kill
    tar, zip, unzip

Practice SSH and file transfer:

    ssh user@server
    scp file.txt user@server:/path/
    rsync -av folder/ user@server:/path/

------------------------------------------------------------------------

# PHASE 1 --- PYTHON PACKAGING

## 1.1 src-layout

Create project using src-layout.

## 1.2 pyproject.toml

Must include:

-   Metadata
-   Dependencies (fastapi, uvicorn, pydantic, prometheus_client)
-   CLI entrypoint

Example:

    [project]
    name = "appcore"
    version = "0.1.0"
    dependencies = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "prometheus_client"
    ]

    [project.scripts]
    appcore-serve = "appcore.cli:serve"

Install:

    pip install -e .

------------------------------------------------------------------------

# PHASE 2 --- NETWORKING

Understand:

-   IP address
-   Port
-   TCP vs UDP
-   DNS
-   HTTP vs HTTPS

Practice:

    ip a
    ss -tulnp
    netstat -tulnp
    ping google.com
    curl localhost:8000
    nslookup google.com

Learn difference between:

    127.0.0.1
    0.0.0.0

------------------------------------------------------------------------

# PHASE 3 --- REST + FASTAPI

## Required Endpoints

GET /health\
GET /version\
POST /predict

Use Pydantic models for request/response.

Use correct HTTP status codes.

Implement middleware for logging.

------------------------------------------------------------------------

# PHASE 4 --- DOCKER

## Dockerfile Requirements

-   Use python:3.11-slim
-   Set WORKDIR
-   Copy pyproject and src
-   Install dependencies
-   Expose port 8000
-   Run uvicorn

Build:

    docker build -t production-service .

Run:

    docker run -p 8000:8000 production-service

------------------------------------------------------------------------

# PHASE 5 --- CI

Create GitHub Actions workflow:

    .github/workflows/ci.yml

Must:

-   Install dependencies
-   Run tests
-   Fail on test failure
-   Build Docker image

------------------------------------------------------------------------

# PHASE 6 --- CD

Extend CI to:

-   Build Docker image
-   Push to registry
-   SSH into VM
-   Pull image
-   Restart container

------------------------------------------------------------------------

# PHASE 7 --- MONITORING

Implement Prometheus metrics:

-   Request counter
-   Latency histogram
-   Error counter

Expose:

    /metrics

------------------------------------------------------------------------

# PHASE 8 --- VERSIONING

Create VERSION file.\
Expose version via API.\
Tag releases using:

    git tag v0.1.0

------------------------------------------------------------------------

# FINAL REQUIREMENTS

Your system must:

-   Run locally
-   Run in Docker
-   Run on remote server
-   Pass CI tests
-   Expose metrics
-   Handle errors correctly
-   Use structured logging
-   Follow REST principles

If any item is missing → project incomplete.

------------------------------------------------------------------------

# SUGGESTED 8-WEEK PLAN

Week 1--2: Linux + Packaging\
Week 3: REST + FastAPI\
Week 4: Networking\
Week 5: Docker\
Week 6: CI\
Week 7: CD\
Week 8: Monitoring + Versioning

------------------------------------------------------------------------

END OF SPECIFICATION
