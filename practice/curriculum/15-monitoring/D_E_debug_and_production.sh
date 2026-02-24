#!/bin/bash
# =============================================================================
# Section 15 — Monitoring: Debug Lab (D1-D5) + Production (E1)
# Guide: docs/curriculum/15-monitoring-observability.md
# =============================================================================

# Exercise 7.D.1 — Metrics Not Showing Up
# Symptom: /metrics endpoint works but Prometheus shows no data
# TODO: Check:
# - Prometheus targets (http://localhost:9090/targets)
# - Is the app accessible from Prometheus container? (use docker network)
# - Is metrics_path correct?
# - Is the scrape interval too long?

# Exercise 7.D.2 — Cardinality Explosion
# Symptom: Prometheus memory keeps growing
# TODO: Check for high-cardinality labels:
# BAD:  labels(path=request.url)  ← Every unique URL creates a series!
# GOOD: labels(endpoint="/health") ← Fixed set of endpoints

# Exercise 7.D.3 — Logs Not Structured
# Symptom: Logs are unreadable in production (print statements everywhere)
# TODO: Replace print() with structured logging
# BAD:  print(f"Error: {e}")
# GOOD: logger.error("Request failed", extra={"error": str(e), "request_id": rid})

# Exercise 7.D.4 — Dashboard Shows No Data
# Symptom: Grafana dashboard queries return empty
# TODO: Check:
# - Prometheus data source configured in Grafana?
# - Metric name matches? (check /metrics endpoint)
# - Time range correct?
# - PromQL query syntax?

# Exercise 7.D.5 — Alert Fatigue
# Symptom: Too many false-positive alerts
# TODO: Fix:
# - Add for: 5m to avoid transient spikes
# - Use rate() over longer windows
# - Set meaningful thresholds based on baseline

# ---- PART E: Production Simulation ----
# Exercise 7.E.1 — Full Observability Stack
# TODO: Run the complete monitoring stack:
# docker compose up --build    (app + prometheus + grafana)
# 
# Verify:
# 1. App: http://localhost:8000/health
# 2. Metrics: http://localhost:8000/metrics
# 3. Prometheus: http://localhost:9090 → Targets should be UP
# 4. Grafana: http://localhost:3000 → Import dashboard
#
# Load test:
# for i in $(seq 1 100); do curl -s http://localhost:8000/predict -X POST -H "Content-Type: application/json" -d '{"feature1":1,"feature2":2,"feature3":3}' & done
# wait
# Check Grafana for request spike visualization
