# =============================================================================
# Section 13 — Capstone: Production-Ready ML Service
# Guide: docs/curriculum/13-capstone-project.md
#
# This is the capstone project that ties everything together.
# Build the complete practical-production-service from scratch.
# Integrates ALL sections: Python, Linux, Networking, REST, FastAPI,
# Docker, CI/CD, Monitoring, Git, Database, Security, Infrastructure, Nginx.
# =============================================================================

# Directory Structure (create this):
#
# practical-production-service/
# ├── pyproject.toml
# ├── Dockerfile
# ├── docker-compose.yml
# ├── .dockerignore
# ├── .env.example                   ← Environment template (Section 10)
# ├── .gitignore                     ← Git ignore rules (Section 08)
# ├── .github/
# │   └── workflows/
# │       └── ci.yml
# ├── configs/
# │   └── nginx.conf                 ← Nginx reverse proxy config (Section 12)
# ├── infra/
# │   └── terraform/
# │       └── main.tf                ← IaC config generation (Section 11)
# ├── scripts/
# │   └── health_check.sh            ← Deployment health check (Section 11)
# ├── prometheus.yml
# ├── src/
# │   └── appcore/
# │       ├── __init__.py
# │       ├── api/
# │       │   ├── __init__.py
# │       │   ├── app.py             ← FastAPI application
# │       │   ├── routes.py          ← Route handlers
# │       │   ├── schemas.py         ← Pydantic models
# │       │   ├── dependencies.py    ← Dependency injection
# │       │   ├── middleware.py      ← Custom middleware
# │       │   ├── auth.py            ← API key auth dependency (Section 10)
# │       │   ├── security.py        ← API key verification (Section 10)
# │       │   └── rate_limiter.py    ← Rate limiting logic (Section 10)
# │       ├── db/
# │       │   ├── __init__.py
# │       │   ├── database.py        ← SQLite connection manager (Section 09)
# │       │   ├── repository.py      ← CRUD operations (Section 09)
# │       │   └── cache.py           ← Optional Redis caching (Section 09)
# │       ├── models/
# │       │   ├── __init__.py
# │       │   └── predict.py         ← ML prediction logic
# │       └── monitoring/
# │           ├── __init__.py
# │           ├── metrics.py         ← Prometheus metrics
# │           └── logging.py         ← Structured logging
# └── tests/
#     ├── __init__.py
#     ├── test_health.py
#     ├── test_predict.py
#     ├── test_metrics.py
#     ├── test_db.py                  ← Database tests (Section 09)
#     └── test_auth.py                ← Auth/security tests (Section 10)
