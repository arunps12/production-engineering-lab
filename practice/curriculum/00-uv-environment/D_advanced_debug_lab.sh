#!/usr/bin/env bash
# =============================================================================
# Section 0 — uv & Python Environment: Advanced Debug Lab
# Guide: docs/curriculum/00-uv-python-environment.md
# =============================================================================

# Exercise 0.D.1 — Debug: "Module Not Found" After Install
# Scenario: You installed a package but Python can't find it.
# TODO: Diagnose and fix — check which python, sys.path, .venv activation


# Exercise 0.D.2 — Debug: Conflicting Transitive Dependencies
# Scenario: Two packages require incompatible versions of a shared dependency.
# TODO: Use uv pip list to find the conflict, resolve with constraints


# Exercise 0.D.3 — Debug: Stale .venv with Wrong Python
# Scenario: .venv was created with Python 3.10, project requires 3.12.
# TODO: Detect the problem, recreate with correct version


# Exercise 0.D.4 — Debug: CI Fails but Local Works
# Scenario: Tests pass on your machine but fail in CI.
# TODO: Compare Python versions, installed packages, OS differences


# Exercise 0.D.5 — Debug: Docker Build Fails on 'uv sync'
# Scenario: Dockerfile runs uv sync but it fails.
# TODO: Check Dockerfile for proper COPY order, network access, cache mounts
