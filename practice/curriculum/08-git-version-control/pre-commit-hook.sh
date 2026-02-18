#!/bin/bash
# Exercise 8.C.3 — Pre-commit Hook Template
# Guide: docs/curriculum/08-git-version-control.md
# Save to: .git/hooks/pre-commit

# #!/bin/bash
# set -e
# echo "=== Pre-commit checks ==="
#
# # Lint
# echo "Running linter..."
# ruff check . || { echo "Linting failed!"; exit 1; }
#
# # Format check
# echo "Checking formatting..."
# ruff format --check . || { echo "Formatting failed!"; exit 1; }
#
# # Tests (optional — can be slow)
# # echo "Running tests..."
# # pytest tests/ -x -q || { echo "Tests failed!"; exit 1; }
#
# echo "All checks passed!"
