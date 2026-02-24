"""
Capstone — Tests: Metrics Endpoint
Run: pytest tests/test_metrics.py -v
"""


def test_metrics_endpoint():
    """GET /metrics returns Prometheus metrics."""
    # TODO: response = client.get("/metrics")
    # assert response.status_code == 200
    # assert "http_requests_total" in response.text
    pass


def test_metrics_after_request():
    """Metrics increment after making requests."""
    # TODO: Make a request, then check /metrics for updated counters
    pass
