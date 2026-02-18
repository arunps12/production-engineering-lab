"""
Exercise 4.D.1 — Debug: CSV Encoding Issues
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. Handle CSV files with UTF-8 BOM (byte order mark)
2. Handle files with Latin-1 encoding
3. Write a function that tries multiple encodings
4. Handle special characters in CSV fields
"""

import csv
from io import StringIO


def read_csv_safe(filepath: str, encodings=None) -> str:
    """Try multiple encodings to read a file."""
    if encodings is None:
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    # TODO: Try each encoding, return content on success
    pass


# TODO: Test with a CSV containing special characters
csv_with_unicode = """name,city,notes
José García,São Paulo,Açaí bowl café
Müller,München,Straße → Büro
"""

reader = csv.DictReader(StringIO(csv_with_unicode))
for row in reader:
    print(f"  {row['name']:<15} {row['city']:<12} {row['notes']}")
