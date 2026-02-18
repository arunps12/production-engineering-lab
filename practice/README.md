# Practice Exercises

This directory contains starter files for every exercise in the curriculum and Python guide.
Each file has a docstring referencing the guide section, a brief task description, and `TODO` markers where you should write code.

## How to Use

1. Read the corresponding guide section in `docs/`
2. Open the practice file
3. Fill in the `TODO` sections
4. Run/test your solution

## Directory Structure

```
practice/
├── python-guide/          ← Python fundamentals exercises
│   ├── 01-foundations/        (22 files — variables, strings, loops, functions)
│   │   ├── B01–B12              Part B: Beginner
│   │   ├── C01–C06              Part C: Intermediate
│   │   ├── D01–D03              Part D: Debug Lab
│   │   └── E_expense_tracker    Part E: Mini-Project
│   ├── 02-core-python-skills/ (16 files — classes, modules, decorators)
│   ├── 03-debugging/          (14 files — stack traces, pdb, logging)
│   └── 04-data-and-apis/      (15 files — file I/O, CSV, JSON, APIs)
│
└── curriculum/            ← Production engineering exercises
    ├── 00-uv-environment/     (6 files — uv, virtual envs, pyproject.toml)
    ├── 01-linux/              (7 files — filesystem, processes, scripting)
    ├── 02-networking/         (8 files — TCP/IP, DNS, sockets, ports)
    ├── 03-rest-api/           (4 files — HTTP methods, Pydantic, OpenAPI)
    ├── 04-fastapi/            (11 files — endpoints, middleware, testing, DI)
    │   └── E_complete_api/        Full production API scaffold
    ├── 05-docker/             (6 files — Dockerfile, compose, debugging)
    ├── 06-cicd/               (4 files — GitHub Actions, pipelines)
    ├── 07-monitoring/         (4 files — logging, Prometheus, Grafana)
    └── 08-capstone/           (16 files — complete production service)
        ├── src/appcore/           Application code scaffold
        ├── tests/                 Test stubs
        ├── Dockerfile             Multi-stage build template
        ├── docker-compose.yml     Full stack compose
        └── verify.sh              Verification script
```

## Exercise Naming Convention

| Prefix | Level | Description |
|--------|-------|-------------|
| `B##_` | Beginner | Foundational exercises |
| `C##_` | Intermediate | Real-world patterns |
| `D##_` | Debug Lab | Find and fix bugs |
| `E_`   | Production | End-to-end simulations |

## File Counts

| Section | Files | Exercises |
|---------|-------|-----------|
| Python Guide: Foundations | 22 | 22 |
| Python Guide: Core Skills | 16 | 16 |
| Python Guide: Debugging | 14 | 14 |
| Python Guide: Data & APIs | 15 | 15 |
| Curriculum: uv Environment | 6 | 24 |
| Curriculum: Linux | 7 | 51 |
| Curriculum: Networking | 8 | 27 |
| Curriculum: REST API Design | 4 | 18 |
| Curriculum: FastAPI | 11 | 20 |
| Curriculum: Docker | 6 | 23 |
| Curriculum: CI/CD | 4 | 18 |
| Curriculum: Monitoring | 4 | 19 |
| Curriculum: Capstone | 16 | 16 |
| **Total** | **133** | **~283** |

> Some sections group multiple exercises into a single file (e.g., Linux bash exercises are grouped by range).

## Reference Guides

- [Python Guide](../docs/python-guide/)
- [Curriculum](../docs/curriculum/)
