#!/usr/bin/env bash
# =============================================================================
# Section 0 — uv & Python Environment: Beginner Exercises
# Guide: docs/curriculum/00-uv-python-environment.md
# =============================================================================

# Exercise 0.B.1 — Install uv
# TODO: Install uv using the official installer
# curl -LsSf https://astral.sh/uv/install.sh | sh
# uv --version


# Exercise 0.B.2 — Create a New Project
# TODO: Create a new Python project with uv
# uv init practical-production-service
# cd practical-production-service
# ls -la


# Exercise 0.B.3 — Create a Virtual Environment
# TODO: Create and inspect a virtual environment
# uv venv
# source .venv/bin/activate
# which python


# Exercise 0.B.4 — Set Up src-layout
# TODO: Create the src layout directory structure
# mkdir -p src/appcore
# touch src/appcore/__init__.py


# Exercise 0.B.5 — Configure pyproject.toml
# TODO: Edit pyproject.toml with proper metadata
# See the guide for the complete configuration


# Exercise 0.B.6 — Add Dependencies
# TODO: Add project dependencies
# uv add fastapi uvicorn


# Exercise 0.B.7 — Install the Project in Editable Mode
# TODO: Install in editable mode and verify
# uv pip install -e .
# python -c "import appcore; print('OK')"


# Exercise 0.B.8 — Add a Dev Dependency
# TODO: Add development dependencies
# uv add --dev pytest httpx


# Exercise 0.B.9 — Write and Run a Minimal Test
# TODO: Create and run a test
# See B09_minimal_test.py in this directory


# Exercise 0.B.10 — Understand 'uv run'
# TODO: Run commands through uv
# uv run python -c "import sys; print(sys.executable)"
# uv run pytest
