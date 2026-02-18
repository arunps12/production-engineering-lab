"""
Section 7 — Monitoring: Intermediate Exercises (C1-C6)
Guide: docs/curriculum/07-monitoring-observability.md
"""

# Exercise 7.C.1 — Custom Metrics Module
# TODO: Create a reusable metrics module

# from prometheus_client import Counter, Histogram, Gauge, Info
#
# class AppMetrics:
#     def __init__(self, app_name: str = "production_service"):
#         self.request_count = Counter(
#             f"{app_name}_requests_total",
#             "Total HTTP requests",
#             ["method", "endpoint", "status_code"]
#         )
#         self.request_duration = Histogram(
#             f"{app_name}_request_duration_seconds",
#             "HTTP request duration",
#             ["method", "endpoint"]
#         )
#         self.active_requests = Gauge(
#             f"{app_name}_active_requests",
#             "Currently active requests"
#         )
#         self.model_info = Info(
#             f"{app_name}_model",
#             "Model information"
#         )
#
#     def record_request(self, method, endpoint, status_code, duration):
#         self.request_count.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
#         self.request_duration.labels(method=method, endpoint=endpoint).observe(duration)


# Exercise 7.C.2 — Metrics Middleware
# TODO: Create FastAPI middleware that auto-records metrics for every request


# Exercise 7.C.3 — Business Metrics
# TODO: Add prediction-specific metrics:
# - prediction_count (Counter)
# - prediction_confidence (Histogram)
# - prediction_latency (Histogram)
# - model_version (Info)


# Exercise 7.C.4 — Prometheus Configuration
# TODO: See prometheus.yml file


# Exercise 7.C.5 — Grafana Dashboard
# TODO: Create a Grafana dashboard JSON (see grafana_dashboard.json)


# Exercise 7.C.6 — Alerting Rules
# TODO: Define alerting rules for:
# - High error rate (>5% of requests are 5xx)
# - High latency (p99 > 2s)
# - Service down (health check failing)
