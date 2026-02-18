"""
Exercise 3.B.2 — Fix These Bugs
Guide: docs/python-guide/03-debugging.md

Each function has exactly one bug. Find and fix it.
"""


def calculate_discount(price, discount_percent):
    """Apply discount and return new price."""
    return price * discount_percent / 100  # Should subtract from price


def find_common(list1, list2):
    """Find common elements."""
    common = []
    for item in list1:
        if item in list1:  # Wrong list!
            common.append(item)
    return common


def count_char(text, char):
    """Count occurrences of char in text."""
    count = 0
    for c in text:
        if c == char:
            count += 1
        return count  # Indentation bug — returns too early


def safe_divide(a, b):
    """Divide a by b, return 0 if b is zero."""
    if b == 0:
        return 0
    return b / a  # Arguments reversed


# TODO: Fix each bug and verify with tests
