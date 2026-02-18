#!/usr/bin/env bash
# =============================================================================
# Section 2 — Networking: Intermediate Exercises
# Guide: docs/curriculum/02-networking-debug-lab.md
# =============================================================================

# Exercise 2.C.1 — Python HTTP Server and Inspect Traffic
# TODO: python3 -m http.server 8080 &
# TODO: curl -v http://localhost:8080


# Exercise 2.C.2 — Connection Refused vs Timeout
# TODO: curl http://localhost:1 (refused) vs curl --connect-timeout 2 http://192.0.2.1 (timeout)


# Exercise 2.C.3 — 0.0.0.0 vs 127.0.0.1 Experiment
# See C03_bind_experiment.py


# Exercise 2.C.4 — DNS Failure Simulation
# TODO: curl http://nonexistent-domain-12345.com, observe the error


# Exercise 2.C.5 — HTTP Headers Deep Dive
# TODO: curl -I, curl -H "Authorization: Bearer token", curl -H "Accept: application/json"


# Exercise 2.C.6 — Port Scanning (Your Own Machine)
# TODO: for port in {8000..8010}; do (echo >/dev/tcp/localhost/$port) 2>/dev/null && echo "$port open"; done


# Exercise 2.C.7 — Measure Latency
# TODO: ping -c 10 google.com | tail -1
# TODO: curl -o /dev/null -s -w "Total: %{time_total}s\n" https://google.com


# Exercise 2.C.8 — TCP Connection States
# See C08_connection_states.py
