"""
Exercise 4.C.4 — Retry and Rate Limiting
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. Implement api_call_with_retry with exponential backoff
2. Handle: connection errors, timeouts, 429 (rate limited), 500+ (server errors)
3. Don't retry on 4xx client errors (except 429)
4. Test with httpbin.org endpoints
"""

import time
import requests


def api_call_with_retry(url: str, max_retries: int = 3, backoff_factor: float = 1.0, timeout: int = 10):
    """Make an API call with exponential backoff retry."""
    # TODO: Implement retry logic
    pass


# TODO: Test with successful endpoint
# response = api_call_with_retry("https://httpbin.org/get")

# TODO: Test with server error endpoint
# response = api_call_with_retry("https://httpbin.org/status/500", backoff_factor=0.5)
