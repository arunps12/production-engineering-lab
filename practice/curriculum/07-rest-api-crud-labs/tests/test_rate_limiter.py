"""Tests for rate limiter."""

from src.crud_api.rate_limiter import RateLimiter


def test_rate_limiter_allows_within_limit():
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    for _ in range(5):
        assert limiter.allow("client1") is True


def test_rate_limiter_blocks_over_limit():
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    for _ in range(3):
        assert limiter.allow("client1") is True
    assert limiter.allow("client1") is False


def test_rate_limiter_per_client():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    assert limiter.allow("client1") is True
    assert limiter.allow("client1") is True
    assert limiter.allow("client1") is False
    # Different client still allowed
    assert limiter.allow("client2") is True


def test_rate_limiter_reset():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    limiter.allow("client1")
    limiter.allow("client1")
    assert limiter.allow("client1") is False
    limiter.reset()
    assert limiter.allow("client1") is True
