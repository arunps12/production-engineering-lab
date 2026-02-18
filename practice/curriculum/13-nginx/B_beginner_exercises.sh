#!/bin/bash
# =============================================================================
# Section 13 — Nginx: Beginner Exercises (B1-B6)
# Guide: docs/curriculum/13-nginx-reverse-proxy.md
# =============================================================================

# Exercise 13.B.1 — Run Nginx in Docker
# TODO: docker run -d --name nginx -p 80:80 nginx:latest
# TODO: curl http://localhost
# TODO: docker stop nginx && docker rm nginx

# Exercise 13.B.2 — Custom Nginx Configuration
# TODO: See nginx-basic.conf in this directory
# docker run -d --name nginx -p 80:80 \
#   -v $PWD/nginx-basic.conf:/etc/nginx/nginx.conf:ro nginx:latest

# Exercise 13.B.3 — Reverse Proxy to FastAPI
# TODO: See nginx-proxy.conf and docker-compose.yml

# Exercise 13.B.4 — Serve Static Files
# TODO: Add location /static/ block to nginx config

# Exercise 13.B.5 — View Nginx Logs
# TODO: docker exec nginx tail -f /var/log/nginx/access.log
# TODO: docker exec nginx tail -f /var/log/nginx/error.log

# Exercise 13.B.6 — Test Configuration
# TODO: docker exec nginx nginx -t
# TODO: docker exec nginx nginx -s reload
