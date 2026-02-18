"""
Exercise 4.B.2 — Working with CSV
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. Write a list of dicts to CSV using DictWriter
2. Read CSV using DictReader
3. Note that CSV values are always strings (convert types!)
4. Calculate statistics from CSV data
"""

import csv

# Sample data
students = [
    {"name": "Alice", "age": 22, "grade": "A", "gpa": 3.9},
    {"name": "Bob", "age": 25, "grade": "B", "gpa": 3.2},
    {"name": "Charlie", "age": 21, "grade": "A", "gpa": 3.8},
    {"name": "Diana", "age": 23, "grade": "C", "gpa": 2.5},
]

# TODO: Write students to /tmp/students.csv


# TODO: Read students back from CSV


# TODO: Convert types (age → int, gpa → float)


# TODO: Calculate and print average GPA and honor roll (GPA >= 3.5)
