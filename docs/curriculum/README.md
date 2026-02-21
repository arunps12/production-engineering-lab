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

| Section | Topic | File |
|---------|-------|------|
| 0 | UV + Python Environment | [00-uv-python-environment.md](00-uv-python-environment.md) |
| 1 | Linux Fundamentals | [01-linux-fundamentals.md](01-linux-fundamentals.md) |
| 2 | Networking & Debug Lab | [02-networking-debug-lab.md](02-networking-debug-lab.md) |
| 3 | REST API Design | [03-rest-api-design.md](03-rest-api-design.md) |
| 4 | FastAPI Professional Practice | [04-fastapi-professional.md](04-fastapi-professional.md) |
| 5 | Docker & Containerization | [05-docker-containerization.md](05-docker-containerization.md) |
| 6 | CI/CD Automation | [06-ci-cd-automation.md](06-ci-cd-automation.md) |
| 7 | Monitoring & Observability | [07-monitoring-observability.md](07-monitoring-observability.md) |
| 8 | Git & Version Control | [08-git-version-control.md](08-git-version-control.md) |
| 9 | Database Fundamentals | [09-database-fundamentals.md](09-database-fundamentals.md) |
| 10 | Security Fundamentals | [10-security-fundamentals.md](10-security-fundamentals.md) |
| 11 | Cloud & Infrastructure Basics | [11-cloud-infrastructure-basics.md](11-cloud-infrastructure-basics.md) |
| 12 | Nginx & Reverse Proxy | [12-nginx-reverse-proxy.md](12-nginx-reverse-proxy.md) |
| 13 | Final Capstone | [13-capstone-project.md](13-capstone-project.md) |

### Extended Practice Modules

| Section | Topic | File |
|---------|-------|------|
| 14 | PostgreSQL Production Labs | [14-postgresql-production.md](14-postgresql-production.md) |
| 15 | Elasticsearch Practice | [15-elasticsearch-practice.md](15-elasticsearch-practice.md) |
| 16 | RDF & SPARQL Labs | [16-rdf-sparql-labs.md](16-rdf-sparql-labs.md) |
| 17 | REST API CRUD Labs | [17-rest-api-crud-labs.md](17-rest-api-crud-labs.md) |
| 18 | Docker Debug Labs | [18-docker-debug-labs.md](18-docker-debug-labs.md) |
| 19 | Ansible Practice | [19-ansible-practice.md](19-ansible-practice.md) |
| 20 | CI/CD Practice | [20-cicd-practice.md](20-cicd-practice.md) |

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
│       │   ├── auth.py             # API key auth (Section 10)
│       │   ├── security.py         # Key verification (Section 10)
│       │   └── rate_limiter.py     # Rate limiting (Section 10)
│       ├── db/
│       │   ├── database.py         # SQLite manager (Section 09)
│       │   ├── repository.py       # CRUD operations (Section 09)
│       │   └── cache.py            # Redis cache (Section 09)
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
│       └── main.tf                 # IaC config (Section 11)
│
├── tests/
├── scripts/
│   ├── run_local.sh
│   ├── deploy.sh
│   └── health_check.sh            # Health verification (Section 11)
├── Dockerfile
├── docker-compose.yml
├── .env.example                    # Environment template (Section 10)
├── .gitignore                      # Git rules (Section 08)
├── .github/workflows/ci.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Suggested 14-Week Plan

| Week | Focus |
|------|-------|
| 1 | Section 0 (uv) + Section 1 (Linux) — first half |
| 2 | Section 1 (Linux) — second half + Section 2 (Networking) |
| 3 | Section 3 (REST Design) + Section 4 (FastAPI) — first half |
| 4 | Section 4 (FastAPI) — second half |
| 5 | Section 5 (Docker) |
| 6 | Section 6 (CI/CD) |
| 7 | Section 7 (Monitoring) |
| 8 | Section 8 (Git) + Section 9 (Databases) |
| 9 | Section 10 (Security) + Section 11 (Cloud) |
| 10 | Section 12 (Nginx) + Section 13 (Capstone) |
| 11 | Section 14 (PostgreSQL) + Section 15 (Elasticsearch) |
| 12 | Section 16 (RDF/SPARQL) + Section 17 (REST CRUD) |
| 13 | Section 18 (Docker Debug) + Section 19 (Ansible) |
| 14 | Section 20 (CI/CD Practice) — pipeline integration |

---

## Environment Requirements

- Linux (native, WSL2, or VM)
- Python 3.11+
- `uv` (installed via `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker + Docker Compose
- Git
- `curl`, `jq`, `ss`, `netstat` (standard Linux tools)
- Ansible (`pip install ansible`) — for Section 19

---

## Completion Criteria

By the end, you must be able to:

- [ ] Explain *why* each tool exists (not just commands)
- [ ] Diagnose failures without guessing
- [ ] Rebuild environments reproducibly from scratch
- [ ] Deploy a containerized service with CI/CD and monitoring
- [ ] Explain these concepts clearly in a technical interview
