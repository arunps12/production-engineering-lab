# =============================================================================
# Section 11 — Auth & Security Tests
# Guide: docs/curriculum/20-capstone-project.md
#
# Exercise: Write tests for authentication and rate limiting.
#
# TODO:
# 1. Test /predict returns 403 without API key
# 2. Test /predict returns 403 with wrong API key
# 3. Test /predict succeeds with valid API key
# 4. Test rate limiter allows requests within limit
# 5. Test rate limiter blocks requests over limit
# =============================================================================

# from fastapi.testclient import TestClient
# from appcore.api.app import app
# from appcore.api.rate_limiter import InMemoryRateLimiter


# client = TestClient(app)


# def test_predict_requires_api_key():
#     """POST /predict without key should return 403."""
#     # TODO: response = client.post("/predict", json={"text": "test"})
#     # TODO: assert response.status_code == 403
#     pass


# def test_predict_rejects_bad_key():
#     """POST /predict with wrong key should return 403."""
#     # TODO: Implement
#     pass


# def test_predict_accepts_valid_key(monkeypatch):
#     """POST /predict with correct key should succeed."""
#     # TODO: monkeypatch API_KEY env var, send request with X-API-Key header
#     pass


# def test_rate_limiter_allows():
#     """Requests within the window should be allowed."""
#     # TODO: limiter = InMemoryRateLimiter(max_requests=5, window_seconds=60)
#     # TODO: assert all allowed for 5 requests
#     pass


# def test_rate_limiter_blocks():
#     """Requests over the limit should be blocked."""
#     # TODO: limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)
#     # TODO: 3rd request should return False
#     pass
