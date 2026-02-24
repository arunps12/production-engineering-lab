# Production Engineering Bootcamp — Curriculum Index

**Author:** Arun
**Goal:** Become a Production-Ready Backend / ML Systems Engineer
**Mode:** Execution-Based Learning (Theory → Practice → Debug → Simulate)

---

## How to Use This Curriculum

1. Work through each section **in order** — later sections depend on earlier ones.
2. Read the **THEORY** first. Do not skip it. Understanding *why* is more valuable than knowing *how*.
3. Complete **Beginner → Intermediate → Advanced → Production** exercises progressively.
4. Everything builds toward **ONE evolving project**: `practical-production-service/`.
5. All Python work uses **`uv`** — no raw `pip`.

---

## Curriculum Map

### Core Foundations (Sections 0–3)

| Section | Topic | File |
|---------|-------|------|
| 0 | UV + Python Environment | [00-uv-python-environment.md](00-uv-python-environment.md) |
| 1 | Linux Fundamentals | [01-linux-fundamentals.md](01-linux-fundamentals.md) |
| 2 | Git & Version Control | [02-git-version-control.md](02-git-version-control.md) |
| 3 | Networking & Debug Lab | [03-networking-debug-lab.md](03-networking-debug-lab.md) |

### Data & API Development (Sections 4–8)

| Section | Topic | File |
|---------|-------|------|
| 4 | Database Fundamentals | [04-database-fundamentals.md](04-database-fundamentals.md) |
| 4b | SQL Mastery | [04b-sql-mastery.md](04b-sql-mastery.md) |
| 5 | REST API Design | [05-rest-api-design.md](05-rest-api-design.md) |
| 6 | FastAPI Professional Practice | [06-fastapi-professional.md](06-fastapi-professional.md) |
| 7 | REST API CRUD Labs | [07-rest-api-crud-labs.md](07-rest-api-crud-labs.md) |
| 8 | PostgreSQL Production Labs | [08-postgresql-production.md](08-postgresql-production.md) |

### Deployment & Infrastructure (Sections 9–14)

| Section | Topic | File |
|---------|-------|------|
| 9 | Docker & Containerization | [09-docker-containerization.md](09-docker-containerization.md) |
| 10 | Docker Debug Labs | [10-docker-debug-labs.md](10-docker-debug-labs.md) |
| 11 | Security Fundamentals | [11-security-fundamentals.md](11-security-fundamentals.md) |
| 12 | Nginx & Reverse Proxy | [12-nginx-reverse-proxy.md](12-nginx-reverse-proxy.md) |
| 13 | CI/CD Automation | [13-ci-cd-automation.md](13-ci-cd-automation.md) |
| 14 | CI/CD Practice | [14-cicd-practice.md](14-cicd-practice.md) |

### Operations & Advanced Topics (Sections 15–19)

| Section | Topic | File |
|---------|-------|------|
| 15 | Monitoring & Observability | [15-monitoring-observability.md](15-monitoring-observability.md) |
| 16 | Cloud & Infrastructure Basics | [16-cloud-infrastructure-basics.md](16-cloud-infrastructure-basics.md) |
| 17 | Ansible Practice | [17-ansible-practice.md](17-ansible-practice.md) |
| 18 | Elasticsearch Practice | [18-elasticsearch-practice.md](18-elasticsearch-practice.md) |
| 19 | RDF & SPARQL Labs | [19-rdf-sparql-labs.md](19-rdf-sparql-labs.md) |

### Final Integration (Section 20)

| Section | Topic | File |
|---------|-------|------|
| 20 | Capstone Project | [20-capstone-project.md](20-capstone-project.md) |

---

## Target Project Structure

```
practical-production-service/
│
├── src/
│   └── appcore/
│       ├── __init__.py
│       ├── cli.py
│       ├── logic.py
│       ├── api/
│       │   ├── app.py
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   ├── dependencies.py
│       │   ├── auth.py             # API key auth (Section 11)
│       │   ├── security.py         # Key verification (Section 11)
│       │   └── rate_limiter.py     # Rate limiting (Section 11)
│       ├── db/
│       │   ├── database.py         # SQLite manager (Section 04)
│       │   ├── repository.py       # CRUD operations (Section 04)
│       │   └── cache.py            # Redis cache (Section 04)
│       ├── config/
│       │   └── settings.py
│       └── monitoring/
│           └── metrics.py
│
├── configs/
│   ├── config.yaml
│   └── nginx.conf                  # Reverse proxy (Section 12)
│
├── infra/
│   └── terraform/
│       └── main.tf                 # IaC config (Section 16)
│
├── tests/
├── scripts/
│   ├── run_local.sh
│   ├── deploy.sh
│   └── health_check.sh            # Health verification (Section 16)
├── Dockerfile
├── docker-compose.yml
├── .env.example                    # Environment template (Section 11)
├── .gitignore                      # Git rules (Section 02)
├── .github/workflows/ci.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Suggested 14-Week Plan

| Week | Focus |
|------|-------|
| 1 | Section 0 (uv) + Section 1 (Linux) |
| 2 | Section 2 (Git) + Section 3 (Networking) |
| 3 | Section 4 (Database) + Section 4b (SQL Mastery) + Section 5 (REST Design) |
| 4 | Section 6 (FastAPI) + Section 7 (REST CRUD Labs) |
| 5 | Section 8 (PostgreSQL) + Section 9 (Docker) |
| 6 | Section 10 (Docker Debug) + Section 11 (Security) |
| 7 | Section 12 (Nginx) + Section 13 (CI/CD) |
| 8 | Section 14 (CI/CD Practice) + Section 15 (Monitoring) |
| 9 | Section 16 (Cloud) + Section 17 (Ansible) |
| 10 | Section 18 (Elasticsearch) + Section 19 (RDF/SPARQL) |
| 11–14 | Section 20 (Capstone Project) — full integration build |

---

## Environment Requirements

- Linux (native, WSL2, or VM)
- Python 3.11+
- `uv` (installed via `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker + Docker Compose
- Git
- `curl`, `jq`, `ss`, `netstat` (standard Linux tools)
- Ansible (`pip install ansible`) — for Section 17

---

## Completion Criteria

By the end, you must be able to:

- [ ] Explain *why* each tool exists (not just commands)
- [ ] Diagnose failures without guessing
- [ ] Rebuild environments reproducibly from scratch
- [ ] Deploy a containerized service with CI/CD and monitoring
- [ ] Explain these concepts clearly in a technical interview
