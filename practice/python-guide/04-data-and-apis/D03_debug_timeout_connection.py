"""
Exercise 4.D.3 — Debug: Timeout and Connection Handling
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. Simulate and handle: timeout, 404, 500, connection refused, DNS failure
2. Map each failure to the correct exception type
3. Provide helpful error messages for each case
"""

import requests


def demonstrate_failure_modes():
    """Test various network failure scenarios."""
    test_cases = [
        ("Timeout", "https://httpbin.org/delay/10", {"timeout": 2}),
        ("404 Not Found", "https://httpbin.org/status/404", {"timeout": 5}),
        ("500 Server Error", "https://httpbin.org/status/500", {"timeout": 5}),
        ("Connection Refused", "http://localhost:1", {"timeout": 2}),
    ]

    for label, url, kwargs in test_cases:
        print(f"\n  {label}:")
        # TODO: Try each request and handle the specific exception
        # Print the exception type and a helpful fix suggestion


# TODO: Run the demonstration
# demonstrate_failure_modes()
