"""
PART E — Production Simulation: Data Processing CLI Tool
Guide: docs/python-guide/04-data-and-apis.md

Build a complete tool that:
1. Reads employee data from CSV
2. Validates and cleans the data
3. Analyzes by department
4. Writes JSON report
5. Prints human-readable summary

Acceptance Criteria:
- [ ] Reads CSV with proper error handling
- [ ] Validates all input data (required fields, types, ranges)
- [ ] Produces clean JSON output
- [ ] Handles edge cases (empty file, all invalid rows, missing columns)
- [ ] Prints readable summary
- [ ] No function longer than 25 lines
- [ ] All major functions have docstrings
- [ ] Uses 'with' for all file operations
"""

import csv
import json
import sys
from datetime import datetime
from pathlib import Path


def read_employees(filepath: str) -> tuple:
    """Read employee data from CSV. Returns (employees, errors)."""
    # TODO: Implement
    pass


def analyze_employees(employees: list) -> dict:
    """Analyze employees and return summary stats."""
    # TODO: Implement
    pass


def write_report(report: dict, filepath: str) -> int:
    """Write report to JSON file. Returns file size."""
    # TODO: Implement
    pass


def print_summary(report: dict):
    """Print human-readable summary."""
    # TODO: Implement
    pass


def main():
    """Main pipeline: Read → Analyze → Write → Print."""
    # TODO: Create sample CSV if no args provided
    # TODO: Run the pipeline
    pass


if __name__ == "__main__":
    main()
