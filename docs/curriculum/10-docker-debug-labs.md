# SECTION 10 — DOCKER DEBUG LABS

---

## PART A — CONCEPT EXPLANATION

### Why Docker Debugging Skills Matter

In production engineering, Docker containers **will** break. You need a systematic approach to diagnose and fix issues quickly. Common failure modes include:

```
┌─────────────────────────────────────────────┐
│            Docker Failure Taxonomy           │
├─────────────────────────────────────────────┤
│ 1. Container won't start (exit code 1/137)  │
│ 2. Container starts but service unreachable │
│ 3. Health check failing (unhealthy status)  │
│ 4. Container keeps restarting (crash loop)  │
│ 5. Containers can't talk to each other      │
│ 6. Data lost after restart (no volumes)     │
│ 7. Port conflicts (address already in use)  │
│ 8. Permission denied on mounted volumes     │
│ 9. Out of memory (OOM killed)               │
│ 10. Image pull failures                     │
└─────────────────────────────────────────────┘
```

### The Debug Checklist

Always follow a systematic approach — don't guess:

```bash
# Step 1: Container status
docker compose ps -a
# Look for: Exit codes, health status, restart count

# Step 2: Logs
docker compose logs <service>
# Look for: Error messages, stack traces, connection refused

# Step 3: Inspect
docker inspect <container>
# Look for: Mounts, environment, network settings, health check

# Step 4: Network
docker network ls
docker network inspect <network>
# Look for: Correct network attachment, IP assignments

# Step 5: Shell in
docker compose exec <service> sh
# Look for: File permissions, DNS resolution, process state

# Step 6: Resources
docker stats --no-stream
# Look for: Memory usage, CPU, blocked I/O

# Step 7: Ports
docker port <container>
ss -tlnp | grep <port>
# Look for: Port conflicts, wrong bindings

# Step 8: Volumes
docker volume ls
docker volume inspect <volume>
# Look for: Missing mounts, permission issues
```

### Reading Container Exit Codes

| Exit Code | Meaning | Common Cause |
|-----------|---------|-------------|
| 0 | Success | Container completed its task |
| 1 | Application error | Crash, unhandled exception |
| 126 | Permission denied | Cannot execute entrypoint |
| 127 | Command not found | Wrong entrypoint/cmd |
| 137 | Killed (SIGKILL) | OOM killed or `docker kill` |
| 139 | Segfault (SIGSEGV) | Memory corruption |
| 143 | Terminated (SIGTERM) | Graceful shutdown |

### Docker Networking — How Containers Talk

```
docker-compose.yml:
  services:
    app:       ──→ hostname: "app"
    postgres:  ──→ hostname: "postgres"
    redis:     ──→ hostname: "redis"
```

Within a Docker Compose network, services resolve each other **by service name**:

```
app can connect to:
  postgres:5432    ✓  (service name as hostname)
  localhost:5432   ✗  (different container!)
  db:5432          ✗  (wrong hostname — must match service name)
  127.0.0.1:5432   ✗  (points to app's own loopback)
```

**Most common mistake:** Using `localhost` or `127.0.0.1` in one container to reach another container. Use the service name instead.

### Health Checks

Health checks tell Docker whether a service is actually working:

```yaml
services:
  postgres:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U labuser"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**Health check states:**
- `starting` — Container just started, health check hasn't run yet
- `healthy` — Last health check passed
- `unhealthy` — Health check failed N consecutive times

**depends_on with health check:**
```yaml
services:
  app:
    depends_on:
      postgres:
        condition: service_healthy  # Wait for PG to be ready
```

### Volume Permissions

Linux containers run as specific users. Volume permission issues occur when:

```
Host directory:  drwxr-xr-x  root:root  /data
Container user:  appuser (uid 1000)
Result:          Permission denied when writing to /data
```

**Fixes:**
1. Match UIDs: `RUN chown 1000:1000 /data`
2. Use Docker volumes instead of bind mounts
3. Set `user: "1000:1000"` in compose

### Memory Limits

Containers can be OOM-killed when they exceed memory limits:

```yaml
services:
  elasticsearch:
    deploy:
      resources:
        limits:
          memory: 1G
    environment:
      ES_JAVA_OPTS: "-Xms512m -Xmx512m"  # JVM heap ≤ 50% of container limit
```

**Rule:** JVM heap should be at most 50% of container memory — the JVM needs the other 50% for off-heap memory, file caches, etc.

### Common Beginner Misunderstandings

1. **"The container is running so the service is working"** — A running container doesn't mean the application inside is healthy. Always use health checks.
2. **"`localhost` refers to other containers"** — In Docker, `localhost` is the container itself. Use service names for inter-container communication.
3. **"Data persists in containers"** — Container filesystems are ephemeral. Without volumes, data is lost on restart.
4. **"`docker compose restart` fixes everything"** — Restarting won't fix configuration errors. Read the logs first.
5. **"Port 5432 is always available"** — Check for port conflicts with `ss -tlnp`. Another container or host service may already be using the port.

---

## PART B — BEGINNER PRACTICE

### Exercise 18.B.1 — DB Hostname Wrong (Connection Failure)

A FastAPI app can't connect to Postgres because the `DATABASE_HOST` doesn't match the service name.

```bash
cd practice/curriculum/18-docker-debug-labs
docker compose -f exercises/ex18_1_broken.yml up -d
docker compose -f exercises/ex18_1_broken.yml logs app
```

**Symptom:** `could not translate host name "database" to address`

**Debug steps:**
1. Check the compose file — what hostname does the app expect?
2. What is the Postgres service named?
3. They don't match — fix `DATABASE_HOST` to match the service name

**Practice files:**
- `practice/curriculum/18-docker-debug-labs/exercises/ex18_1_broken.yml`
- `practice/curriculum/18-docker-debug-labs/solutions/ex18_1_fixed.yml`

### Exercise 18.B.2 — Healthcheck Failing

Postgres keeps showing `unhealthy` because `pg_isready` uses the wrong username.

```bash
docker compose -f exercises/ex18_2_broken.yml up -d
docker inspect pg_health_lab --format='{{json .State.Health}}' | jq .
```

**Symptom:** Health check exit code 1, status `unhealthy`

**Practice files:**
- `practice/curriculum/18-docker-debug-labs/exercises/ex18_2_broken.yml`
- `practice/curriculum/18-docker-debug-labs/solutions/ex18_2_fixed.yml`

### Exercise 18.B.3 — Learn the Debug Commands

Practice each debug command on a running stack:

```bash
# Start a known-good stack
docker compose up -d

# Practice each command
docker compose ps -a
docker compose logs postgres
docker inspect <container_id>
docker network ls
docker compose exec postgres sh -c "pg_isready -U labuser"
docker stats --no-stream
docker port <container_id>
docker volume ls
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 18.C.1 — Volume Permission Error

An Nginx container can't write logs because the mounted directory has wrong permissions.

```bash
docker compose -f exercises/ex18_3_broken.yml up -d
docker compose -f exercises/ex18_3_broken.yml logs nginx
```

**Symptom:** `Permission denied` when writing to `/var/log/nginx/`

**Debug steps:**
1. Check what the volume mount looks like
2. Shell into the container and check permissions: `ls -la /var/log/nginx/`
3. Fix: Adjust directory permissions or switch to a Docker named volume

**Practice files:**
- `practice/curriculum/18-docker-debug-labs/exercises/ex18_3_broken.yml`
- `practice/curriculum/18-docker-debug-labs/solutions/ex18_3_fixed.yml`

### Exercise 18.C.2 — Elasticsearch OOM

ES crashes because the container memory limit is too low for the JVM heap.

```bash
docker compose -f exercises/ex18_4_broken.yml up -d
docker compose -f exercises/ex18_4_broken.yml logs elasticsearch
docker inspect es_mem_lab --format='{{.State.OOMKilled}}'
```

**Symptom:** Container exits with code 137 (OOM killed) or ES fails to start

**Practice files:**
- `practice/curriculum/18-docker-debug-labs/exercises/ex18_4_broken.yml`
- `practice/curriculum/18-docker-debug-labs/solutions/ex18_4_fixed.yml`

### Exercise 18.C.3 — Port Collision

Two services try to bind to the same host port.

```bash
docker compose -f exercises/ex18_5_broken.yml up -d
docker compose -f exercises/ex18_5_broken.yml logs
```

**Symptom:** `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Debug steps:**
1. Check which services use port 8080
2. Fix: Change one service to a different host port

**Practice files:**
- `practice/curriculum/18-docker-debug-labs/exercises/ex18_5_broken.yml`
- `practice/curriculum/18-docker-debug-labs/solutions/ex18_5_fixed.yml`

---

## PART D — ADVANCED DEBUG LAB

### Exercise 18.D.1 — Multi-Service Dependency Failure

**Symptom:** App container starts before Postgres is ready and crashes with a connection error. With `restart: always`, it enters a crash loop.

**Task:**
1. Observe the crash loop: `docker compose ps -a` (restart count increasing)
2. Add `depends_on` with `condition: service_healthy`
3. Add a proper health check to Postgres
4. Verify the app waits for Postgres to be healthy before starting

### Exercise 18.D.2 — DNS Resolution Failure

**Symptom:** App logs show `Name or service not known`.

**Task:**
1. Check if all services are on the same Docker network
2. Check for typos in service names
3. Verify with: `docker compose exec app nslookup postgres`
4. Fix network configuration

### Exercise 18.D.3 — Compose File Syntax Error

**Symptom:** `docker compose up` fails with a YAML parse error or unexpected field error.

**Task:**
1. Read the error message — it includes the line number
2. Common issues: wrong indentation, tab characters, duplicate keys
3. Validate: `docker compose config` to check syntax before running
4. Fix the YAML and re-run

### Exercise 18.D.4 — Container Exit Code Investigation

**Symptom:** Container exits with code 126 or 127.

**Task:**
1. Check exit code: `docker inspect <container> --format='{{.State.ExitCode}}'`
2. 126 = permission denied on entrypoint, 127 = command not found
3. Shell into the image: `docker run --rm -it <image> sh`
4. Check entrypoint: `docker inspect <image> --format='{{json .Config.Entrypoint}}'`
5. Fix the entrypoint or command

### Exercise 18.D.5 — Network Isolation Debug

**Symptom:** Two compose stacks can't communicate with each other.

**Task:**
1. Each `docker compose up` creates its own network
2. Services in different networks can't reach each other
3. Fix: Create an external network and add both stacks to it
4. Verify with `docker network inspect`

---

## PART E — PRODUCTION SIMULATION

### Scenario: Production Docker Debugging On-Call

You're the on-call engineer. A production Docker Compose deployment has multiple issues. Debug and fix all of them:

1. **Service A** (app) can't connect to **Service B** (postgres) — wrong hostname
2. **Service B** health check is failing — wrong user in `pg_isready`
3. **Service C** (nginx) has permission errors — volume mounts with wrong permissions
4. **Service D** (elasticsearch) keeps OOM crashing — memory limits too low
5. **Port conflict** — two services fighting for port 8080

For each issue:
- Run the broken compose file
- Use the debug checklist systematically
- Identify the root cause
- Fix and verify
- Document the diagnosis in your notes

```bash
# Your debugging toolkit
docker compose -f <file> ps -a         # Status
docker compose -f <file> logs <svc>    # Logs
docker inspect <container> | jq .      # Details
docker compose -f <file> exec <svc> sh # Shell in
docker stats --no-stream               # Resources
docker network inspect <net>           # Networking
```

---

## Key Takeaways

1. **Follow the checklist** — Don't guess. Go through status → logs → inspect → network → shell → resources.
2. **Service names are hostnames** — Use Compose service names for inter-container communication, never `localhost`.
3. **Health checks are mandatory** — A running container doesn't mean a working service.
4. **Exit codes tell you what happened** — 137 = OOM, 127 = command not found, 1 = application error.
5. **Volumes persist data** — Without volumes, container restarts lose everything.
6. **`docker compose config`** — Validate your compose file before running it.

---
*Next: [Section 11 — Security Fundamentals](11-security-fundamentals.md)*
