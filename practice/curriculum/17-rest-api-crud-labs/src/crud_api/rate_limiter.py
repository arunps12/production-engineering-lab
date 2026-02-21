"""Simple in-memory rate limiter using sliding window."""

import time
from collections import defaultdict


class RateLimiter:
    """Token-bucket-style rate limiter per client key."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def allow(self, client_key: str) -> bool:
        """Check if a request from client_key is allowed."""
        now = time.time()
        cutoff = now - self.window_seconds

        # Remove expired timestamps
        self._requests[client_key] = [
            ts for ts in self._requests[client_key] if ts > cutoff
        ]

        if len(self._requests[client_key]) >= self.max_requests:
            return False

        self._requests[client_key].append(now)
        return True

    def reset(self):
        """Reset all rate limit state (for testing)."""
        self._requests.clear()
