# =============================================================================
# Section 10 — Rate Limiter
# Guide: docs/curriculum/13-capstone-project.md
#
# Exercise: Implement a sliding window rate limiter.
#
# TODO:
# 1. Implement InMemoryRateLimiter class:
#    - __init__(max_requests: int, window_seconds: int)
#    - is_allowed(client_id: str) -> bool
#      - Track request timestamps per client_id
#      - Remove expired entries outside the window
#      - Return True if under limit, False otherwise
# 2. Create a FastAPI middleware that:
#    - Extracts client IP from request
#    - Calls is_allowed()
#    - Returns 429 Too Many Requests if rate limited
# =============================================================================

import time
from collections import defaultdict


class InMemoryRateLimiter:
    """Sliding window rate limiter."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if the client is within the rate limit."""
        # TODO: Implement sliding window logic
        pass
