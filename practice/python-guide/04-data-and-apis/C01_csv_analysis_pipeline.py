"""
Exercise 4.C.1 — CSV Data Analysis Pipeline
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
Build a complete pipeline: Read CSV → Clean → Analyze → Report

1. Load CSV data and handle invalid rows
2. Clean/normalize the data
3. Analyze: totals, averages, by category
4. Print a formatted report with bars
"""

import csv
from collections import defaultdict
from io import StringIO

RAW_DATA = """date,product,category,quantity,unit_price,region
2024-01-05,Laptop,Electronics,2,999.99,North
2024-01-05,Mouse,Electronics,10,29.99,North
2024-01-06,Desk,Furniture,3,249.99,South
2024-01-06,Chair,Furniture,5,199.99,South
2024-01-07,Laptop,Electronics,1,999.99,East
2024-01-07,Keyboard,Electronics,8,79.99,East
2024-01-08,Desk,Furniture,2,249.99,North
2024-01-08,Monitor,Electronics,4,399.99,West
2024-01-09,Chair,Furniture,,199.99,South
2024-01-09,Laptop,Electronics,3,999.99,West
2024-01-10,Mouse,Electronics,invalid,29.99,North
"""


def load_and_clean(raw_csv: str) -> tuple:
    """Load CSV, clean data, return (records, error_count)."""
    # TODO: Implement
    pass


def analyze(records: list) -> dict:
    """Analyze records and return summary stats."""
    # TODO: Implement
    pass


def print_report(summary: dict):
    """Print formatted report."""
    # TODO: Implement
    pass


# TODO: Run the pipeline
