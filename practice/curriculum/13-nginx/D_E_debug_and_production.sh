#!/bin/bash
# =============================================================================
# Section 13 — Nginx: Debug Lab (D1-D5) + Production (E1)
# Guide: docs/curriculum/13-nginx-reverse-proxy.md
# =============================================================================

# Exercise 13.D.1 — Debug: 502 Bad Gateway
# Symptom: Client gets 502 from Nginx
# TODO: Check:
# [ ] Is the app running? (docker ps)
# [ ] Is proxy_pass URL correct?
# [ ] Can Nginx reach the app? (docker network)
# docker exec nginx curl http://app:8000/health

# Exercise 13.D.2 — Debug: Upstream Timeout (504)
# Symptom: Slow endpoints return 504
# TODO: Add timeout directives:
# proxy_connect_timeout 60s;
# proxy_send_timeout 60s;
# proxy_read_timeout 60s;

# Exercise 13.D.3 — Debug: Real IP Not Forwarded
# Symptom: App logs show 172.17.0.1 (Docker) instead of real client IP
# TODO: Add proxy_set_header X-Real-IP $remote_addr;
# TODO: Configure app to read X-Real-IP header

# Exercise 13.D.4 — Debug: SSL Certificate Expired
# TODO: openssl s_client -connect localhost:443 -servername example.com
# TODO: Check expiry date, renew with certbot

# Exercise 13.D.5 — Debug: Configuration Syntax Error
# TODO: docker exec nginx nginx -t
# Read the error, fix, test again

# --- PRODUCTION ---
# Exercise 13.E.1 — Complete Reverse Proxy Setup
# TODO: docker compose up --build
# Test:
# 1. curl http://localhost/health  (proxied to app)
# 2. Load test: hey -n 5000 -c 100 http://localhost/api/health
# 3. Verify rate limiting kicks in
# 4. Check Nginx access logs for request distribution
