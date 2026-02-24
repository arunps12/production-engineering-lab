# Docker Debugging Checklist

## Step-by-Step Diagnosis

### 1. Container Status

```bash
docker compose ps -a
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Look for: `Exited`, `Restarting`, `unhealthy`

### 2. Logs

```bash
# All services
docker compose logs

# Specific service, follow mode
docker compose logs -f <service>

# Last 50 lines
docker compose logs --tail=50 <service>
```

Common log patterns:
- `connection refused` → service not ready / wrong hostname
- `permission denied` → file/volume ownership issue
- `address already in use` → port collision
- `OOM` / `Cannot allocate memory` → memory limit too low
- `FATAL: role "X" does not exist` → wrong database credentials

### 3. Container Inspection

```bash
# Full inspection
docker inspect <container>

# Health status
docker inspect --format='{{json .State.Health}}' <container> | jq .

# Environment variables
docker inspect --format='{{json .Config.Env}}' <container> | jq .

# Network settings
docker inspect --format='{{json .NetworkSettings.Networks}}' <container> | jq .

# Mounts
docker inspect --format='{{json .Mounts}}' <container> | jq .
```

### 4. Networking

```bash
# List networks
docker network ls

# Inspect network (see connected containers + IPs)
docker network inspect <network>

# DNS resolution from inside container
docker exec <container> nslookup <service_name>

# Connectivity test
docker exec <container> ping -c 2 <other_service>
docker exec <container> curl -sf http://<service>:<port>/health
```

### 5. Interactive Debugging

```bash
# Shell into running container
docker exec -it <container> sh    # or bash

# Run diagnostic commands inside
apt-get update && apt-get install -y curl net-tools  # if needed
netstat -tlnp
curl localhost:<port>
env | grep DATABASE
cat /etc/hosts
```

### 6. Resource Issues

```bash
# Real-time stats
docker stats

# Disk usage
docker system df

# Check memory limits
docker inspect --format='{{.HostConfig.Memory}}' <container>

# Check OOM kills
docker inspect --format='{{.State.OOMKilled}}' <container>
```

### 7. Volume & File Issues

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume>

# Check file permissions inside container
docker exec <container> ls -la /path/to/dir

# Check host-side mount
ls -la ./mounted-dir/
```

### 8. Port Issues

```bash
# Check port mappings
docker port <container>

# Check host port usage
ss -tlnp | grep <port>
lsof -i :<port>
```

## Common Fixes Quick Reference

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Connection refused | Wrong hostname | Use compose service name as hostname |
| Container exits immediately | CMD/entrypoint error | Check logs, fix command |
| Health: unhealthy | Wrong health check | Fix `healthcheck` command/user/port |
| Permission denied | UID mismatch | Match `user:` in compose or fix ownership |
| OOM killed | Memory limit too low | Increase `deploy.resources.limits.memory` |
| Port already allocated | Port collision | Change host port mapping |
| Volume empty | Wrong mount path | Check `volumes:` paths |
| DNS resolution fails | Not on same network | Ensure services share a compose network |
