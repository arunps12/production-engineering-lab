# Module 18 — Docker Debug Labs

## Goals

- Diagnose and fix common Docker Compose failures
- Master debugging tools: `docker logs`, `docker inspect`, `docker exec`
- Build a systematic debugging checklist
- Practice 5 real-world failure scenarios with guided solutions

## Prerequisites

- Docker & Docker Compose installed
- Basic Docker knowledge (Module 5)

## How This Module Works

Each exercise provides an **intentionally broken** `docker-compose.yml` in `exercises/`.
Your job is to:

1. Run the broken compose file
2. Observe the failure
3. Use the debug checklist to diagnose
4. Fix the issue
5. Verify the fix
6. Compare with the reference solution in `solutions/`

---

## Debug Checklist

Use this checklist for **every** Docker debugging scenario:

```bash
# 1. Check container status
docker compose -f <file> ps -a

# 2. Read container logs
docker compose -f <file> logs <service>

# 3. Inspect container details
docker inspect <container_name>

# 4. Check networking
docker network ls
docker network inspect <network>

# 5. Shell into a running container
docker compose -f <file> exec <service> sh

# 6. Check resource usage
docker stats --no-stream

# 7. Check port bindings
docker port <container_name>
ss -tlnp | grep <port>

# 8. Check volumes
docker volume ls
docker volume inspect <volume>
```

See also: [debug_checklist.md](debug_checklist.md)

---

## Exercise 18.1 — DB Hostname Wrong (Connection Failure)

### Scenario

A FastAPI app cannot connect to Postgres because the hostname is wrong.

### Steps

1. Start the broken stack:

```bash
docker compose -f exercises/ex18_1_broken.yml up -d
```

2. Check status:

```bash
docker compose -f exercises/ex18_1_broken.yml ps -a
```

3. Check app logs:

```bash
docker compose -f exercises/ex18_1_broken.yml logs app
```

Expected error: `could not translate host name "database" to address`

4. **Diagnose:** The app connects to hostname `database`, but the service is named `postgres` in compose.

5. **Fix:** The `DATABASE_HOST` environment variable should match the compose service name.

6. Apply the fix:

```bash
docker compose -f exercises/ex18_1_broken.yml down
docker compose -f solutions/ex18_1_fixed.yml up -d
```

7. Verify:

```bash
docker compose -f solutions/ex18_1_fixed.yml logs app
# Should show: "Connected to database successfully"
```

---

## Exercise 18.2 — Healthcheck Failing

### Scenario

A Postgres container keeps restarting because the healthcheck command is wrong.

### Steps

1. Start:

```bash
docker compose -f exercises/ex18_2_broken.yml up -d
```

2. Watch the health status:

```bash
watch -n 2 'docker compose -f exercises/ex18_2_broken.yml ps'
```

3. Check healthcheck output:

```bash
docker inspect pg_health_lab --format='{{json .State.Health}}' | jq .
```

Expected: status `unhealthy`, exit code 1.

4. **Diagnose:** The healthcheck runs `pg_isready -U wronguser`, but the Postgres user is `labuser`.

5. **Fix:** Correct the healthcheck user.

6. Verify with the fixed version:

```bash
docker compose -f exercises/ex18_2_broken.yml down
docker compose -f solutions/ex18_2_fixed.yml up -d
docker inspect pg_health_lab --format='{{.State.Health.Status}}'
# Expected: healthy
```

---

## Exercise 18.3 — Volume Permission Issue

### Scenario

An app container fails to write to a mounted volume due to permission mismatch.

### Steps

1. Start:

```bash
docker compose -f exercises/ex18_3_broken.yml up -d
```

2. Check logs:

```bash
docker compose -f exercises/ex18_3_broken.yml logs writer
```

Expected error: `Permission denied: '/data/output.log'`

3. **Diagnose:** The container runs as a non-root user (UID 1000) but the volume directory is owned by root.

4. **Fix options:**
   - Add an init script that fixes permissions
   - Use `user:` directive matching host UID
   - Pre-create the directory with correct ownership

5. Verify:

```bash
docker compose -f exercises/ex18_3_broken.yml down -v
docker compose -f solutions/ex18_3_fixed.yml up -d
docker compose -f solutions/ex18_3_fixed.yml logs writer
# Expected: "Write successful"
```

---

## Exercise 18.4 — Container Memory Too Low (Elasticsearch)

### Scenario

Elasticsearch fails to start because the JVM heap exceeds the container memory limit.

### Steps

1. Start:

```bash
docker compose -f exercises/ex18_4_broken.yml up -d
```

2. Check status:

```bash
docker compose -f exercises/ex18_4_broken.yml ps -a
```

Expected: ES container is restarting or exited.

3. Check logs:

```bash
docker compose -f exercises/ex18_4_broken.yml logs es
```

Expected: OOM-related error or JVM startup failure.

4. Check resource usage:

```bash
docker stats --no-stream
```

5. **Diagnose:** `ES_JAVA_OPTS=-Xms1g -Xmx1g` but container memory limit is 256m.

6. **Fix:** Either increase container memory limit or reduce JVM heap.

7. Verify:

```bash
docker compose -f exercises/ex18_4_broken.yml down -v
docker compose -f solutions/ex18_4_fixed.yml up -d
curl -s http://localhost:9201/_cluster/health | jq .status
# Expected: "yellow" or "green"
```

---

## Exercise 18.5 — Port Collision

### Scenario

Two services try to bind to the same host port, causing one to fail.

### Steps

1. Start:

```bash
docker compose -f exercises/ex18_5_broken.yml up -d
```

2. Check status:

```bash
docker compose -f exercises/ex18_5_broken.yml ps -a
```

Expected: One container started, the other failed with port bind error.

3. Check logs:

```bash
docker compose -f exercises/ex18_5_broken.yml logs
```

Expected error: `Bind for 0.0.0.0:8080 failed: port is already allocated`

4. **Diagnose:** Both `web1` and `web2` map to host port 8080.

5. **Fix:** Map services to different host ports (8080 and 8081).

6. Verify:

```bash
docker compose -f exercises/ex18_5_broken.yml down
docker compose -f solutions/ex18_5_fixed.yml up -d
curl -s http://localhost:8080
curl -s http://localhost:8081
```

---

## Cleanup

```bash
# Clean up all exercises
for f in exercises/ex18_*_broken.yml solutions/ex18_*_fixed.yml; do
    docker compose -f "$f" down -v 2>/dev/null
done
```

## Deliverables

- [exercises/](exercises/) — 5 intentionally broken compose files
- [solutions/](solutions/) — 5 corrected compose files
- [debug_checklist.md](debug_checklist.md) — systematic debugging reference

## Next Steps

- Module 19: Ansible Practice
- Module 20: CI/CD Practice
