"""
Exercise 2.C.5 — Building a Real Module: validators
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Create a validators module with reusable validation functions
2. Write validate_email, validate_age, validate_url
3. Return validation results as (is_valid, error_message) tuples
4. Make it importable from other files
"""

import re
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate an email address. Returns (is_valid, error_message)."""
    # TODO: Implement with regex or simple checks
    pass


def validate_age(age, min_age: int = 0, max_age: int = 150) -> Tuple[bool, Optional[str]]:
    """Validate age is a valid integer in range."""
    # TODO: Implement
    pass


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """Validate a URL starts with http:// or https://."""
    # TODO: Implement
    pass


def validate_password(password: str, min_length: int = 8) -> Tuple[bool, Optional[str]]:
    """Validate password strength."""
    # TODO: Implement (length, has uppercase, has digit, etc.)
    pass


# TODO: Test all validators
if __name__ == "__main__":
    test_cases = [
        ("email", "user@example.com"),
        ("email", "invalid-email"),
        ("age", 25),
        ("age", -5),
        ("url", "https://example.com"),
        ("url", "not-a-url"),
    ]
    # TODO: Run and print results
