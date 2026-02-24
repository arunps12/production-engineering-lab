# Production Engineering Lab

Hands-on Linux, Docker, Networking, FastAPI, CI/CD, Git, Database, Security, Nginx & Cloud practice lab — learn production engineering by building real systems.

## Overview

Two complete learning tracks — **Learn Python** and **Production Engineering Bootcamp**. Every section follows a structured learning path:

> **Theory → Beginner Practice → Intermediate Practice → Advanced Debug Lab → Production Simulation**

By the end you will have built `practical-production-service` — a fully containerized, tested, monitored, and CI/CD-deployed Python API — from scratch.

## Learn Python Guide

Start here if you're new to Python or want to solidify fundamentals before diving into production engineering.

| # | Section | Topics |
|---|---------|--------|
| 1 | [Foundations](docs/python-guide/01-foundations.md) | Variables, types, loops, functions, lists, dicts, sets, clean code |
| 2 | [Core Python Skills](docs/python-guide/02-core-python-skills.md) | OOP, classes, modules, virtual environments, error handling |
| 3 | [Debugging (Superpower)](docs/python-guide/03-debugging.md) | Stack traces, variable tracing, pdb, logic errors, refactoring |
| 4 | [Data & APIs](docs/python-guide/04-data-and-apis.md) | CSV, JSON, HTTP requests, external APIs, edge cases |
| 5 | [Testing with Pytest](docs/python-guide/05-testing-with-pytest.md) | Unit tests, fixtures, mocking, parametrize, TDD, coverage |
| 6 | [Concurrency & Async](docs/python-guide/06-concurrency-async.md) | Threading, multiprocessing, asyncio, async/await, event loops |
| 7 | [System Automation & Scripting](docs/python-guide/07-system-automation-scripting.md) | subprocess, pathlib, CLI tools, file ops, cron, log parsing |

See the [Python Guide README](docs/python-guide/README.md) for the full learning path and schedule.

## Production Engineering Curriculum

### Core Foundations

| # | Section | Topics |
|---|---------|--------|
| 0 | [UV & Python Environment](docs/curriculum/00-uv-python-environment.md) | `uv`, `pyproject.toml`, lockfiles, reproducible builds, virtual environments |
| 1 | [Linux Fundamentals](docs/curriculum/01-linux-fundamentals.md) | Processes, ports, permissions, shells, daemons, systemd concepts |
| 2 | [Git & Version Control](docs/curriculum/02-git-version-control.md) | Branching, rebasing, hooks, tags, conventional commits, Git workflows |
| 3 | [Networking & Debug Lab](docs/curriculum/03-networking-debug-lab.md) | IP, DNS, TCP handshake, sockets, `127.0.0.1` vs `0.0.0.0`, firewalls |

### Data & API Development

| # | Section | Topics |
|---|---------|--------|
| 4 | [Database Fundamentals](docs/curriculum/04-database-fundamentals.md) | SQLite, connection management, repository pattern, migrations, Redis caching |
| 5 | [REST API Design](docs/curriculum/05-rest-api-design.md) | HTTP verbs, status codes, idempotency, pagination, versioning |
| 6 | [FastAPI Professional Practice](docs/curriculum/06-fastapi-professional.md) | ASGI, uvicorn, middleware, dependency injection, async, testing |
| 7 | [REST API CRUD Labs](docs/curriculum/07-rest-api-crud-labs.md) | Full CRUD API, PUT vs PATCH, pagination, rate limiting, idempotency, pytest suite |
| 8 | [PostgreSQL Production Labs](docs/curriculum/08-postgresql-production.md) | Docker Postgres, schema design, EXPLAIN ANALYZE, transactions & locks, Alembic migrations |

### Deployment & Infrastructure

| # | Section | Topics |
|---|---------|--------|
| 9 | [Docker & Containerization](docs/curriculum/09-docker-containerization.md) | Images, layers, multi-stage builds, Compose, health checks, networking |
| 10 | [Docker Debug Labs](docs/curriculum/10-docker-debug-labs.md) | 5 intentionally broken Compose setups, systematic debug checklist, fix & verify |
| 11 | [Security Fundamentals](docs/curriculum/11-security-fundamentals.md) | API key auth, rate limiting, secrets management, security headers, OWASP |
| 12 | [Nginx Reverse Proxy](docs/curriculum/12-nginx-reverse-proxy.md) | Reverse proxy, load balancing, rate limiting, TLS, security headers, gzip |
| 13 | [CI/CD Automation](docs/curriculum/13-ci-cd-automation.md) | GitHub Actions, caching, matrix builds, Docker registry, deployment |
| 14 | [CI/CD Practice](docs/curriculum/14-cicd-practice.md) | GitHub Actions workflow, local smoke tests, lint + test + service smoke jobs |

### Operations & Advanced Topics

| # | Section | Topics |
|---|---------|--------|
| 15 | [Monitoring & Observability](docs/curriculum/15-monitoring-observability.md) | Prometheus metrics, histograms, structured logging, alerting concepts |
| 16 | [Cloud & Infrastructure](docs/curriculum/16-cloud-infrastructure-basics.md) | IaC concepts, Terraform basics, health checks, deployment strategies |
| 17 | [Ansible Practice](docs/curriculum/17-ansible-practice.md) | Inventory, bootstrap playbook, deploy & rollback playbooks, Jinja2 templates |
| 18 | [Elasticsearch Practice](docs/curriculum/18-elasticsearch-practice.md) | Full-text search, analyzers, Query DSL, SQL vs ES comparison, reindexing with aliases |
| 19 | [RDF & SPARQL Labs](docs/curriculum/19-rdf-sparql-labs.md) | RDF triples, Turtle format, Fuseki Docker, SPARQL queries, SQL vs SPARQL comparison |

### Final Integration

| # | Section | Topics |
|---|---------|--------|
| 20 | [Capstone Project](docs/curriculum/20-capstone-project.md) | Three-level capstone integrating all sections (Guided → Semi-guided → Production sim) |

The [Curriculum README](docs/curriculum/README.md) has the full learning path, suggested schedule, and target project structure.

### Cheatsheets

| Cheatsheet | Description |
|-----------|-------------|
| [SQL vs SPARQL vs Elasticsearch](docs/cheatsheets/sql_vs_sparql_vs_es.md) | Comparison table, same query in 3 languages, when to use each |
| [CRUD ↔ REST / PUT vs PATCH](docs/cheatsheets/crud_rest_put_patch.md) | CRUD-REST mapping, PUT vs PATCH examples, idempotency, SQL vs SPARQL CRUD |

## Target Project Structure

The curriculum incrementally builds this project:

```
practical-production-service/
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml
├── .env.example               # Environment template (Section 11)
├── .gitignore                  # Git ignore rules (Section 02)
├── .github/workflows/ci.yml
├── configs/
│   ├── prometheus.yml
│   └── nginx.conf              # Reverse proxy config (Section 12)
├── infra/terraform/main.tf     # IaC config (Section 16)
├── scripts/health_check.sh     # Deployment verification (Section 16)
├── src/appcore/
│   ├── __init__.py
│   ├── api/
│   │   ├── app.py              # FastAPI application + middleware
│   │   ├── routes.py           # Endpoint handlers
│   │   ├── schemas.py          # Pydantic models
│   │   ├── dependencies.py     # Dependency injection
│   │   ├── auth.py             # API key auth dependency (Section 11)
│   │   ├── security.py         # Key verification (Section 11)
│   │   └── rate_limiter.py     # Sliding window limiter (Section 11)
│   ├── db/
│   │   ├── database.py         # SQLite connection manager (Section 04)
│   │   ├── repository.py       # CRUD operations (Section 04)
│   │   └── cache.py            # Optional Redis cache (Section 04)
│   ├── models/
│   │   └── predict.py          # Prediction model
│   └── monitoring/
│       └── metrics.py          # Prometheus metrics
└── tests/
    ├── conftest.py
    ├── test_health.py
    ├── test_version.py
    ├── test_predict.py
    ├── test_metrics.py
    ├── test_db.py               # Database tests (Section 04)
    └── test_auth.py             # Auth & security tests (Section 11)
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
