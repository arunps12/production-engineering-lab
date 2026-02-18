"""
Exercise 4.B.4 — Handling Malformed Data
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. Attempt to parse bad JSON and handle JSONDecodeError
2. Parse a CSV with missing/invalid fields
3. Validate data types after parsing
4. Report errors without crashing
"""

import json
import csv
from io import StringIO

# TODO: Try parsing these JSON strings (some are invalid)
bad_json_examples = [
    '{"name": "Alice", "age": 30}',
    '{"name": "Alice", age: 30}',
    '{"name": "Alice", "age": 30,}',
    'not json at all',
    '',
]


# TODO: Parse this CSV with missing/invalid data and report errors
bad_csv = """name,age,city
Alice,30,New York
Bob,,London
Charlie,thirty-five,Tokyo
,25,
"""
