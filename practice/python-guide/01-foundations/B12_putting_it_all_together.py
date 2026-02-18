"""
Exercise 1.B.12 — Putting It All Together: Student Grade Analyzer
Guide: docs/python-guide/01-foundations.md

Tasks:
Build a mini-project that uses variables, loops, functions, lists, dicts, and sets.

Requirements:
1. Store student data (name, grades list)
2. Calculate average grade per student
3. Find the top performer
4. Find subjects where any student scored below 60
5. Print a formatted report
"""

# Sample data
students = {
    "Alice": [85, 92, 78, 90, 88],
    "Bob": [72, 68, 84, 90, 76],
    "Charlie": [95, 98, 92, 87, 94],
    "Diana": [60, 55, 70, 65, 58],
}

subjects = ["Math", "Science", "English", "History", "Art"]


def calculate_average(grades: list) -> float:
    """Calculate the average of a list of grades."""
    # TODO: Implement
    pass


def find_top_performer(students: dict) -> str:
    """Find the student with the highest average."""
    # TODO: Implement
    pass


def find_failing_subjects(students: dict, subjects: list, threshold: int = 60) -> set:
    """Find subjects where any student scored below the threshold."""
    # TODO: Implement
    pass


def print_report(students: dict, subjects: list):
    """Print a formatted grade report."""
    # TODO: Implement
    pass


# TODO: Call your functions and print the report
