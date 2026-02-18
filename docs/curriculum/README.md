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
| 8 | Final Capstone | [08-capstone-project.md](08-capstone-project.md) |
| 9 | Git & Version Control | [09-git-version-control.md](09-git-version-control.md) |
| 10 | Database Fundamentals | [10-database-fundamentals.md](10-database-fundamentals.md) |
| 11 | Security Fundamentals | [11-security-fundamentals.md](11-security-fundamentals.md) |
| 12 | Cloud & Infrastructure Basics | [12-cloud-infrastructure-basics.md](12-cloud-infrastructure-basics.md) |
| 13 | Nginx & Reverse Proxy | [13-nginx-reverse-proxy.md](13-nginx-reverse-proxy.md) |

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
├── uv.lock
└── README.md
```

---

## Suggested 8-Week Plan

| Week | Focus |
|------|-------|
| 1 | Section 0 (uv) + Section 1 (Linux) — first half |
| 2 | Section 1 (Linux) — second half + Section 2 (Networking) |
| 3 | Section 3 (REST Design) + Section 4 (FastAPI) — first half |
| 4 | Section 4 (FastAPI) — second half |
| 5 | Section 5 (Docker) |
| 6 | Section 6 (CI/CD) |
| 7 | Section 7 (Monitoring) |
| 8 | Section 8 (Capstone) — full integration |
| 9 | Section 9 (Git) + Section 10 (Databases) |
| 10 | Section 11 (Security) + Section 12 (Cloud) |
| 11 | Section 13 (Nginx) + Review & polish |

---

## Environment Requirements

- Linux (native, WSL2, or VM)
- Python 3.11+
- `uv` (installed via `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker + Docker Compose
- Git
- `curl`, `jq`, `ss`, `netstat` (standard Linux tools)

---

## Completion Criteria

By the end, you must be able to:

- [ ] Explain *why* each tool exists (not just commands)
- [ ] Diagnose failures without guessing
- [ ] Rebuild environments reproducibly from scratch
- [ ] Deploy a containerized service with CI/CD and monitoring
- [ ] Explain these concepts clearly in a technical interview
