#!/usr/bin/env bash
# =============================================================================
# Section 0 — uv & Python Environment: Intermediate Exercises
# Guide: docs/curriculum/00-uv-python-environment.md
# =============================================================================

# Exercise 0.C.1 — Simulate Dependency Conflict
# TODO: Try adding conflicting packages and observe uv's behavior
# uv add "requests>=2.31" "urllib3<1.26"


# Exercise 0.C.2 — Destroy and Rebuild the Environment
# TODO: Delete .venv, rebuild from lock file
# rm -rf .venv
# uv sync
# uv run python -c "import fastapi; print('Rebuilt!')"


# Exercise 0.C.3 — Audit Your Dependency Tree
# TODO: Inspect installed packages and their dependencies
# uv pip list
# uv pip show fastapi


# Exercise 0.C.4 — Pin Python Version
# TODO: Set requires-python in pyproject.toml and verify
# Check: python --version matches the constraint


# Exercise 0.C.5 — Use Environment Variables with uv run
# TODO: Run Python with environment variables
# APP_ENV=production uv run python -c "import os; print(os.getenv('APP_ENV'))"


# Exercise 0.C.6 — Export Requirements for Comparison
# TODO: Export requirements.txt from uv
# uv pip freeze > requirements.txt
# cat requirements.txt


# Exercise 0.C.7 — Test Lock Staleness
# TODO: Modify pyproject.toml manually and check if uv detects stale lock
# uv lock --check
