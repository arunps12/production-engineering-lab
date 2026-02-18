# =============================================================================
# Section 8 — Capstone: Production-Ready ML Service
# Guide: docs/curriculum/08-capstone-project.md
#
# This is the capstone project that ties everything together.
# Build the complete practical-production-service from scratch.
# =============================================================================

# Directory Structure (create this):
#
# practical-production-service/
# ├── pyproject.toml
# ├── Dockerfile
# ├── docker-compose.yml
# ├── .dockerignore
# ├── .github/
# │   └── workflows/
# │       └── ci.yml
# ├── prometheus.yml
# ├── src/
# │   └── appcore/
# │       ├── __init__.py
# │       ├── api/
# │       │   ├── __init__.py
# │       │   ├── app.py           ← FastAPI application
# │       │   ├── routes.py        ← Route handlers
# │       │   ├── schemas.py       ← Pydantic models
# │       │   ├── dependencies.py  ← Dependency injection
# │       │   └── middleware.py    ← Custom middleware
# │       ├── models/
# │       │   ├── __init__.py
# │       │   └── predict.py      ← ML prediction logic
# │       └── monitoring/
# │           ├── __init__.py
# │           ├── metrics.py      ← Prometheus metrics
# │           └── logging.py      ← Structured logging
# └── tests/
#     ├── __init__.py
#     ├── test_health.py
#     ├── test_predict.py
#     └── test_metrics.py
