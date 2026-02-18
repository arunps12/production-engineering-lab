#!/usr/bin/env bash
# =============================================================================
# Exercise 1.C.16 — Bash Script with Error Handling
# Guide: docs/curriculum/01-linux-fundamentals.md
# =============================================================================

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# TODO: Implement a script that:
# 1. Takes a directory path as argument
# 2. Validates the argument exists and is a directory
# 3. Counts files by extension
# 4. Reports total size
# 5. Handles errors gracefully

usage() {
    echo "Usage: $0 <directory>"
    exit 1
}

# TODO: Check argument count
# [[ $# -eq 1 ]] || usage

# TODO: Validate directory exists
# [[ -d "$1" ]] || { echo "Error: '$1' is not a directory"; exit 1; }

# TODO: Count files by extension


# TODO: Report total size
