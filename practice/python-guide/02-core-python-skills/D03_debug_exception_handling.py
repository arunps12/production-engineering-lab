"""
Exercise 2.D.3 — Debug: Exception Handling Gone Wrong
Guide: docs/python-guide/02-core-python-skills.md

This code has exception handling anti-patterns. Fix them.
"""

import json


# Anti-pattern 1: Bare except (catches EVERYTHING including SystemExit)
def load_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:  # BAD: catches KeyboardInterrupt too!
        return {}


# Anti-pattern 2: Swallowing exceptions silently
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        pass  # Returns None silently!


# Anti-pattern 3: Too broad exception handling
def process_data(data):
    try:
        result = data["key"]["nested"]["value"]
        processed = int(result) * 2
        return processed
    except Exception as e:
        print(f"Error: {e}")
        return None  # Hides whether it was KeyError, TypeError, ValueError...


# TODO: Fix each anti-pattern:
# 1. Use specific exceptions
# 2. Return meaningful values or re-raise
# 3. Handle each exception type separately
