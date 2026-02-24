"""
Section 15 — Monitoring: Beginner Exercises (B1-B7)
Guide: docs/curriculum/15-monitoring-observability.md
"""

# Exercise 7.B.1 — Basic Logging Setup
import logging

# TODO: Configure basic logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
# logger = logging.getLogger(__name__)
# logger.info("Application started")
# logger.warning("Low disk space")
# logger.error("Connection failed")


# Exercise 7.B.2 — Structured Logging with JSON
# TODO: pip install python-json-logger
# import json
# from pythonjsonlogger import jsonlogger
#
# handler = logging.StreamHandler()
# formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s")
# handler.setFormatter(formatter)
# logger = logging.getLogger("structured")
# logger.addHandler(handler)
# logger.info("Request received", extra={"method": "GET", "path": "/health"})


# Exercise 7.B.3 — Log Levels
# TODO: Demonstrate when to use each level
# logger.debug("Variable x = 42")        # Development only
# logger.info("Server started on :8000")  # Normal operation
# logger.warning("Disk 80% full")         # Attention needed
# logger.error("Database connection lost") # Error occurred
# logger.critical("Application crash")     # System down


# Exercise 7.B.4 — Add Logging to FastAPI
# TODO: Add structured logging to your FastAPI middleware
# See practice/curriculum/06-fastapi/B04_middleware.py


# Exercise 7.B.5 — Install Prometheus Client
# TODO: pip install prometheus-client
# from prometheus_client import Counter, Histogram, generate_latest
#
# REQUEST_COUNT = Counter("http_requests_total", "Total requests", ["method", "endpoint", "status"])
# REQUEST_DURATION = Histogram("http_request_duration_seconds", "Request duration")


# Exercise 7.B.6 — Create Basic Metrics
# TODO: Instrument your application
# REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
# with REQUEST_DURATION.time():
#     pass  # Your handler code here


# Exercise 7.B.7 — Expose /metrics Endpoint
# from fastapi import FastAPI
# from fastapi.responses import PlainTextResponse
# app = FastAPI()
#
# @app.get("/metrics")
# async def metrics():
#     return PlainTextResponse(generate_latest())
