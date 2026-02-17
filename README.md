# Production Engineering Lab

Hands-on Linux, Docker, Networking, FastAPI & CI/CD practice lab — learn production engineering by building real systems.

## Overview

A complete **DevOps + Backend Engineering Bootcamp** curriculum. Every section follows a structured learning path:

> **Theory → Beginner Practice → Intermediate Practice → Advanced Debug Lab → Production Simulation**

By the end you will have built `practical-production-service` — a fully containerized, tested, monitored, and CI/CD-deployed Python API — from scratch.

## Curriculum

| # | Section | Topics |
|---|---------|--------|
| 0 | [UV & Python Environment](docs/curriculum/00-uv-python-environment.md) | `uv`, `pyproject.toml`, lockfiles, reproducible builds, virtual environments |
| 1 | [Linux Fundamentals](docs/curriculum/01-linux-fundamentals.md) | Processes, ports, permissions, shells, daemons, systemd concepts |
| 2 | [Networking & Debug Lab](docs/curriculum/02-networking-debug-lab.md) | IP, DNS, TCP handshake, sockets, `127.0.0.1` vs `0.0.0.0`, firewalls |
| 3 | [REST API Design](docs/curriculum/03-rest-api-design.md) | HTTP verbs, status codes, idempotency, pagination, versioning |
| 4 | [FastAPI Professional Practice](docs/curriculum/04-fastapi-professional.md) | ASGI, uvicorn, middleware, dependency injection, async, testing |
| 5 | [Docker & Containerization](docs/curriculum/05-docker-containerization.md) | Images, layers, multi-stage builds, Compose, health checks, networking |
| 6 | [CI/CD Automation](docs/curriculum/06-ci-cd-automation.md) | GitHub Actions, caching, matrix builds, Docker registry, deployment |
| 7 | [Monitoring & Observability](docs/curriculum/07-monitoring-observability.md) | Prometheus metrics, histograms, structured logging, alerting concepts |
| 8 | [Final Capstone](docs/curriculum/08-capstone-project.md) | Three-level capstone integrating all sections (Guided → Semi-guided → Production sim) |

The [Curriculum README](docs/curriculum/README.md) has the full learning path, suggested 8-week schedule, and target project structure.

## Target Project Structure

The curriculum incrementally builds this project:

```
practical-production-service/
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
├── configs/prometheus.yml
├── src/appcore/
│   ├── __init__.py
│   ├── api/
│   │   ├── app.py          # FastAPI application + middleware
│   │   ├── routes.py        # Endpoint handlers
│   │   ├── schemas.py       # Pydantic models
│   │   └── dependencies.py  # Dependency injection
│   ├── models/
│   │   └── predict.py       # Prediction model
│   └── monitoring/
│       └── metrics.py       # Prometheus metrics
└── tests/
    ├── conftest.py
    ├── test_health.py
    ├── test_version.py
    ├── test_predict.py
    └── test_metrics.py
```

## Prerequisites

- Linux/macOS terminal (or WSL2 on Windows)
- [uv](https://docs.astral.sh/uv/) — Python package manager
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- Python 3.11+
- Git & a GitHub account

## Getting Started

```bash
# Clone the repo
git clone <repo-url>
cd production-engineering-lab

# Start with Section 0
open docs/curriculum/00-uv-python-environment.md
```

## License

See [LICENSE](LICENSE) for details.
