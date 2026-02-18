# SECTION 12 — NGINX & REVERSE PROXY

---

## PART A — CONCEPT EXPLANATION

### What is a Reverse Proxy?

A reverse proxy sits between clients and your application servers:

```
Client → Internet → [Reverse Proxy (Nginx)] → [App Server :8000]
                                              → [App Server :8001]
                                              → [App Server :8002]
```

**Why use one?**
- **Load balancing** — Distribute requests across multiple app instances
- **SSL termination** — Handle HTTPS at the proxy, plain HTTP internally
- **Static file serving** — Serve CSS/JS/images without hitting your app
- **Caching** — Cache responses to reduce backend load
- **Rate limiting** — Protect against abuse at the edge
- **Security** — Hide internal topology, add headers, filter requests

### Nginx Architecture

Nginx uses an **event-driven, non-blocking** architecture:

```
Master Process (reads config, manages workers)
├── Worker Process 1 (handles connections)
├── Worker Process 2 (handles connections)
├── Worker Process 3 (handles connections)
└── Worker Process 4 (handles connections)
```

Each worker handles **thousands** of concurrent connections (vs Apache's thread-per-connection model).

### Nginx Configuration Structure

```nginx
# /etc/nginx/nginx.conf

# Global settings
worker_processes auto;          # One per CPU core
events {
    worker_connections 1024;    # Max connections per worker
}

http {
    # HTTP-level settings
    include mime.types;
    default_type application/octet-stream;
    
    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    # Server blocks (virtual hosts)
    server {
        listen 80;
        server_name example.com;
        
        location / {
            proxy_pass http://localhost:8000;
        }
    }
}
```

### Key Concepts

**`server` block** — Defines a virtual host (one per domain/port combination)
**`location` block** — Matches URL patterns within a server
**`upstream` block** — Defines a group of backend servers for load balancing
**`proxy_pass`** — Forward requests to a backend server

### Load Balancing Algorithms

```nginx
upstream backend {
    # Round Robin (default) — Each server gets requests in turn
    server app1:8000;
    server app2:8000;
    server app3:8000;
    
    # Least Connections — Send to server with fewest active connections
    # least_conn;
    
    # IP Hash — Same client always goes to same server (session affinity)
    # ip_hash;
    
    # Weighted — Send more traffic to powerful servers
    # server app1:8000 weight=3;
    # server app2:8000 weight=1;
}
```

### SSL/TLS Termination

```
Client ──HTTPS──→ [Nginx] ──HTTP──→ [App Server]
                  (TLS)              (plain — internal network)
```

This allows your application to remain simple (no SSL code) while clients get HTTPS.

### Common Beginner Misunderstandings

1. **"Nginx is just a web server"** — It's primarily used as a reverse proxy, load balancer, and SSL terminator in production.
2. **"My app should handle HTTPS"** — In most architectures, Nginx or a cloud load balancer handles TLS. Your app speaks plain HTTP internally.
3. **"I don't need a reverse proxy for one server"** — Even with one server, Nginx provides SSL, static files, rate limiting, and buffering.
4. **"Load balancing means I need Kubernetes"** — Nginx load balancing with Docker is sufficient for many production workloads.
5. **"proxy_pass is the same as redirect"** — `proxy_pass` forwards the request server-side. A redirect sends the client to a new URL.

---

## PART B — BEGINNER PRACTICE

### Exercise 12.B.1 — Run Nginx in Docker

```bash
docker run -d --name nginx -p 80:80 nginx:latest
curl http://localhost
# You should see the Nginx welcome page
docker stop nginx && docker rm nginx
```

### Exercise 12.B.2 — Custom Nginx Configuration

Create a custom config and mount it:
```nginx
# nginx.conf
events {}
http {
    server {
        listen 80;
        location / {
            return 200 "Hello from Nginx!\n";
            add_header Content-Type text/plain;
        }
    }
}
```

```bash
docker run -d --name nginx \
  -p 80:80 \
  -v $PWD/nginx.conf:/etc/nginx/nginx.conf:ro \
  nginx:latest
curl http://localhost
```

### Exercise 12.B.3 — Reverse Proxy to Your FastAPI App

```nginx
events {}
http {
    server {
        listen 80;
        
        location / {
            proxy_pass http://app:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Docker Compose:
```yaml
services:
  app:
    build: .
    expose:
      - "8000"
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
```

### Exercise 12.B.4 — Serve Static Files

```nginx
server {
    listen 80;
    
    # Static files served directly by Nginx
    location /static/ {
        alias /usr/share/nginx/html/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # API requests proxied to app
    location /api/ {
        proxy_pass http://app:8000;
    }
}
```

### Exercise 12.B.5 — View Nginx Logs

```bash
# Access log — Every request
docker exec nginx tail -f /var/log/nginx/access.log

# Error log — Problems
docker exec nginx tail -f /var/log/nginx/error.log

# Custom log format
log_format custom '$remote_addr - $request_method $request_uri '
                  '$status $body_bytes_sent $request_time';
access_log /var/log/nginx/access.log custom;
```

### Exercise 12.B.6 — Test Configuration

```bash
# Test config syntax before reloading
docker exec nginx nginx -t

# Reload without downtime
docker exec nginx nginx -s reload

# Common error: "test failed" — fix the config, test again
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 12.C.1 — Load Balancing

```nginx
upstream app_servers {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://app_servers;
    }
}
```

Docker Compose with multiple app instances:
```yaml
services:
  app1:
    build: .
    environment:
      INSTANCE_ID: "1"
  app2:
    build: .
    environment:
      INSTANCE_ID: "2"
  app3:
    build: .
    environment:
      INSTANCE_ID: "3"
  nginx:
    image: nginx:latest
    ports: ["80:80"]
    volumes: ["./nginx.conf:/etc/nginx/nginx.conf:ro"]
```

### Exercise 12.C.2 — SSL/TLS with Let's Encrypt

```nginx
server {
    listen 443 ssl;
    server_name example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # Modern SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://app:8000;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Exercise 12.C.3 — Rate Limiting

```nginx
http {
    # Define rate limit zone: 10 requests/second per IP
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    server {
        listen 80;
        
        location /api/ {
            # Allow burst of 20, delay after 10
            limit_req zone=api burst=20 delay=10;
            proxy_pass http://app:8000;
        }
        
        # Health check endpoint — no rate limiting
        location /health {
            proxy_pass http://app:8000;
        }
    }
}
```

### Exercise 12.C.4 — Caching

```nginx
http {
    # Cache zone: 10MB keys, 1GB storage, 60min inactive timeout
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=app_cache:10m
                     max_size=1g inactive=60m;
    
    server {
        listen 80;
        
        location /api/public/ {
            proxy_cache app_cache;
            proxy_cache_valid 200 5m;     # Cache 200s for 5 minutes
            proxy_cache_valid 404 1m;     # Cache 404s for 1 minute
            add_header X-Cache-Status $upstream_cache_status;
            proxy_pass http://app:8000;
        }
        
        # Don't cache authenticated endpoints
        location /api/private/ {
            proxy_no_cache 1;
            proxy_pass http://app:8000;
        }
    }
}
```

### Exercise 12.C.5 — WebSocket Proxying

```nginx
location /ws/ {
    proxy_pass http://app:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400;  # Keep connection open for 24h
}
```

### Exercise 12.C.6 — Gzip Compression

```nginx
http {
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml text/javascript;
    gzip_comp_level 6;
}
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 12.D.1 — Debug: 502 Bad Gateway

Symptom: Nginx returns 502 to clients.
Cause: App server is down, or proxy_pass URL is wrong.
Task: Check `docker ps`, error logs, and `proxy_pass` configuration.

### Exercise 12.D.2 — Debug: Upstream Timeout

Symptom: Slow endpoints return 504 Gateway Timeout.
Task: Increase timeouts:
```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

### Exercise 12.D.3 — Debug: Real IP Not Forwarded

Symptom: App logs show `172.17.0.1` (Docker gateway) instead of real client IP.
Task: Add `proxy_set_header` directives and configure app to read `X-Real-IP`.

### Exercise 12.D.4 — Debug: SSL Certificate Expired

Symptom: `NET::ERR_CERT_DATE_INVALID` in browser.
Task: Check certificate expiry with `openssl`, renew with certbot, reload Nginx.

### Exercise 12.D.5 — Debug: Configuration Syntax Error

Symptom: `nginx -t` fails, service won't start.
Task: Read the error message carefully, fix syntax, test again.

---

## PART E — PRODUCTION SIMULATION

### Scenario: Production-Ready Reverse Proxy

Deploy a complete Nginx setup for your production service:

1. **Reverse proxy** to your FastAPI app (3 instances, load balanced)
2. **SSL termination** with self-signed certs (or Let's Encrypt if you have a domain)
3. **Rate limiting** on API endpoints (10 req/s per IP)
4. **Static file serving** for documentation
5. **Gzip compression** for JSON responses
6. **Health check endpoint** bypasses rate limiting
7. **Access logging** with custom format showing response times
8. **Caching** for public endpoints (5-minute TTL)
9. **Security headers** added by Nginx

Test with load testing tool:
```bash
hey -n 5000 -c 100 http://localhost/api/health
# Verify load is distributed across all 3 instances
# Verify rate limiting kicks in at high concurrency
```

---

## Key Takeaways

1. **Nginx is the gateway to production** — It's the first thing requests hit and the last defense before your app.
2. **SSL termination at the proxy** — Your app speaks HTTP internally, Nginx handles HTTPS externally.
3. **Load balancing is simple** — Nginx upstream blocks distribute traffic across instances.
4. **Rate limiting protects your app** — Set limits per-endpoint based on expected traffic.
5. **Always forward real client IPs** — Without proxy headers, your app logs only see the proxy's IP.
6. **Test config before reloading** — `nginx -t` prevents downtime from syntax errors.

---
*Previous: [Section 11 — Cloud & Infrastructure Basics](11-cloud-infrastructure-basics.md)*
*Next: [Section 13 — Final Capstone](13-capstone-project.md)*
