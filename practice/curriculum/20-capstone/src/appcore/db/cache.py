# =============================================================================
# Section 04 — Optional Redis Cache
# Guide: docs/curriculum/20-capstone-project.md
#
# Exercise (Optional): Add Redis caching for predictions.
#
# TODO:
# 1. Create a Redis client (handle connection failure gracefully)
# 2. Implement cache_get(key) -> dict | None
# 3. Implement cache_set(key, value, ttl=300)
# 4. Use in routes to cache GET /predictions/{id} results
# =============================================================================

import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_redis_client():
    """Return a Redis client, or None if unavailable."""
    # TODO: Connect to Redis, return None on failure
    pass


def cache_get(key: str) -> dict | None:
    """Retrieve cached value."""
    # TODO: GET from Redis, deserialize JSON
    pass


def cache_set(key: str, value: dict, ttl: int = 300) -> None:
    """Store value in cache with TTL."""
    # TODO: SET in Redis with expiration
    pass
