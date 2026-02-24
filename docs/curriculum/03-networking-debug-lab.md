# SECTION 3 — NETWORKING THEORY & DEBUG LAB

---

## PART A — CONCEPT EXPLANATION

### What is an IP Address?

An **IP address** is a numerical label assigned to every device on a network. It serves two purposes:
1. **Identification** — which device is this?
2. **Location** — where in the network is this device?

**IPv4:** 32-bit number written as four octets: `192.168.1.100`
Each octet is 0–255. Total: ~4.3 billion addresses (not enough — hence NAT and IPv6).

**Private vs Public:**

| Range | Type | Usage |
|---|---|---|
| `10.0.0.0/8` | Private | Internal corporate networks |
| `172.16.0.0/12` | Private | Internal networks |
| `192.168.0.0/16` | Private | Home/office networks |
| `127.0.0.0/8` | Loopback | Your own machine |
| Everything else | Public | Internet-routable |

**Mental model:** IP is your mailing address. Port is the apartment number.

### What is DNS?

**DNS** (Domain Name System) translates human-readable names to IP addresses:

```
google.com → 142.250.80.46
```

**How DNS resolution works (simplified):**

```
1. You type "google.com" in browser
2. OS checks /etc/hosts (local override file)
3. OS checks local DNS cache
4. OS asks the configured DNS server (e.g., 8.8.8.8)
5. DNS server asks root nameservers → .com nameservers → google.com nameserver
6. Answer: 142.250.80.46
7. OS caches the result (TTL = Time To Live)
8. Browser connects to 142.250.80.46
```

**Where DNS breaks:**
- `/etc/resolv.conf` points to a dead DNS server → all name resolution fails
- DNS TTL is long → you changed the IP but clients still use the old one
- Inside Docker, containers use Docker's internal DNS (`127.0.0.11`) — host DNS rules don't apply

### What is the TCP Handshake?

TCP is a **reliable**, **ordered**, **connection-oriented** protocol. Before any data flows, the client and server perform a **three-way handshake:**

```
Client                    Server
  │                         │
  │── SYN ──────────────────▶│  "I want to connect"
  │                         │
  │◀──────────── SYN-ACK ──│  "OK, I acknowledge. I also want to connect"
  │                         │
  │── ACK ──────────────────▶│  "I acknowledge your acknowledgment"
  │                         │
  │   Connection established │
  │◀═══ Data flows both ways ═══▶│
```

**Why this matters:**
- If the server isn't listening → client gets `Connection refused`
- If a firewall drops packets → client hangs waiting (no SYN-ACK comes back) → `Connection timed out`
- If the server is overloaded → SYN queue fills up → new connections are dropped silently

### What is a Socket?

A **socket** is an endpoint for communication. It's identified by:

```
(IP address, Port number, Protocol)
```

When Python runs:
```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8000))
s.listen(5)
```

It creates a socket that:
1. Uses IPv4 (`AF_INET`)
2. Uses TCP (`SOCK_STREAM`)
3. Accepts connections from any IP (`0.0.0.0`) on port `8000`
4. Queues up to 5 pending connections

**The kernel manages sockets.** They show up as file descriptors (`/proc/<pid>/fd/`). Every open connection = one file descriptor.

### What Happens When You Open `localhost:8000`?

Complete sequence:

```
1. Browser parses URL: scheme=http, host=localhost, port=8000, path=/
2. DNS resolves "localhost" → 127.0.0.1 (from /etc/hosts)
3. OS creates a TCP socket
4. TCP three-way handshake with 127.0.0.1:8000
5. On success → TCP connection is established
6. Browser sends HTTP request:
     GET / HTTP/1.1
     Host: localhost:8000
     
7. Server (uvicorn) receives the request
8. FastAPI routes it to the handler function
9. Handler returns a response
10. Server sends HTTP response:
      HTTP/1.1 200 OK
      Content-Type: application/json
      
      {"status": "ok"}
      
11. Browser renders the response
12. Connection may be kept alive (HTTP/1.1 keep-alive) or closed
```

### Why `127.0.0.1` vs `0.0.0.0` Matters

This is **the most confusing networking concept** for beginners. Here's the difference:

| Address | Meaning | Who can connect |
|---|---|---|
| `127.0.0.1` (loopback) | Only this machine | Only processes on **this same machine** |
| `0.0.0.0` (all interfaces) | Every network interface | **Anyone** who can reach this machine |

**Example:**
```bash
# Listening on 127.0.0.1:8000
uvicorn app:app --host 127.0.0.1 --port 8000
# ✓ curl http://localhost:8000 (from same machine)
# ✗ curl http://192.168.1.50:8000 (from another machine) → Connection refused

# Listening on 0.0.0.0:8000  
uvicorn app:app --host 0.0.0.0 --port 8000
# ✓ curl http://localhost:8000 (from same machine)
# ✓ curl http://192.168.1.50:8000 (from another machine)
```

**In Docker, this is critical:** A container has its own network stack. If your app listens on `127.0.0.1`, nobody outside the container can reach it — not even the host machine with `-p 8000:8000`. You **must** bind to `0.0.0.0` inside Docker.

### How Firewall Blocks Work

A firewall inspects packets and decides: **allow, drop, or reject**.

```
Incoming packet → Firewall rules → Decision
                                   ├── ACCEPT  → packet reaches the application
                                   ├── DROP    → packet is silently discarded (client times out)
                                   └── REJECT  → packet is refused with an error (client gets immediate error)
```

**Why DROP is worse than REJECT for debugging:** With DROP, the client hangs forever waiting. With REJECT, it gets an immediate `Connection refused`. DROP is more secure (doesn't reveal that a port exists) but harder to debug.

**Common tools:**
- `iptables` — traditional Linux firewall
- `ufw` — Ubuntu's simplified firewall frontend
- `firewalld` — RHEL/CentOS firewall

**Production gotcha:** You deploy to a cloud VM, firewall is set to DROP all except SSH (port 22). Your service on port 8000 is running perfectly — but nobody can reach it. You spend an hour debugging the app before realizing it's the firewall.

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "localhost and 127.0.0.1 are the same in Docker" | Inside a container, localhost only refers to the container itself, not the host |
| "If curl works, the service is reachable from anywhere" | curl from the same machine tests loopback, not external accessibility |
| "Port 8000 is always available" | Check with `ss -tulnp` — another process might hold it |
| "DNS failures mean the internet is down" | It might just be a misconfigured `/etc/resolv.conf` |
| "TCP connection refused = firewall" | Connection refused means the port is reachable but nothing is listening. Firewall causes timeout, not refusal |

---

## PART B — BEGINNER PRACTICE

### Exercise 2.B.1 — Discover Your Network Interfaces

```bash
# Show all network interfaces and their IPs
ip addr show

# Simpler view
ip -brief addr show

# Hostname
hostname
hostname -I  # Show all IP addresses
```

**What to observe:** You'll see `lo` (loopback = 127.0.0.1) and one or more real interfaces (eth0, ens33, etc.) with your machine's IP.

### Exercise 2.B.2 — Test DNS Resolution

```bash
# Resolve a domain
nslookup google.com

# More detail
dig google.com +short

# Check what DNS server you're using
cat /etc/resolv.conf

# Check local hostname overrides
cat /etc/hosts

# Time the DNS resolution
time nslookup google.com
```

### Exercise 2.B.3 — Check Network Connectivity

```bash
# Ping (ICMP echo)
ping -c 4 google.com

# Ping localhost
ping -c 2 127.0.0.1

# Check route to a destination
traceroute google.com 2>/dev/null || tracepath google.com
```

### Exercise 2.B.4 — Explore Listening Ports

```bash
# List all listening TCP/UDP ports
ss -tulnp

# Just TCP
ss -tlnp

# Filter for a specific port
ss -tlnp | grep 22  # SSH
```

**Read the output:**
```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN  0       128     0.0.0.0:22          0.0.0.0:*          users:(("sshd",pid=1234))
```
- `LISTEN` — waiting for connections
- `0.0.0.0:22` — listening on all interfaces, port 22
- `sshd` — the process name

### Exercise 2.B.5 — Make HTTP Requests with curl

```bash
# Basic GET request
curl http://httpbin.org/get

# See response headers
curl -I http://httpbin.org/get

# Verbose mode (shows TCP handshake + HTTP exchange)
curl -v http://httpbin.org/get 2>&1 | head -30

# POST with JSON body
curl -X POST http://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Follow redirects
curl -L http://httpbin.org/redirect/1

# Show only HTTP status code
curl -s -o /dev/null -w "%{http_code}" http://httpbin.org/get
```

### Exercise 2.B.6 — TCP Connection Test with curl Timing

```bash
# Show timing breakdown
curl -w "\
    DNS:        %{time_namelookup}s\n\
    Connect:    %{time_connect}s\n\
    TLS:        %{time_appconnect}s\n\
    Start:      %{time_starttransfer}s\n\
    Total:      %{time_total}s\n\
    HTTP Code:  %{http_code}\n" \
  -s -o /dev/null http://httpbin.org/get
```

**What each timing means:**
- **DNS** — time to resolve the hostname
- **Connect** — time for TCP handshake
- **TLS** — time for TLS handshake (HTTPS only)
- **Start** — time until first byte of response
- **Total** — total request time

### Exercise 2.B.7 — Simulate a Simple TCP Server and Client

```bash
# Terminal 1: Start a TCP server with netcat
# nc -l -p 9999
# (or if that syntax doesn't work):
nc -l 9999 &
NC_PID=$!

sleep 1

# Terminal 2: Connect as a client
echo "Hello from client" | nc localhost 9999

wait $NC_PID 2>/dev/null
```

**What happened:** netcat created a TCP socket, listened on port 9999, accepted a connection, received data, and printed it. This is the simplest possible server.

### Exercise 2.B.8 — Inspect `/etc/hosts`

```bash
cat /etc/hosts

# Add a local alias (requires sudo)
# echo "127.0.0.1 myapp.local" | sudo tee -a /etc/hosts

# Test it
# curl http://myapp.local:8000

# Clean up: remove the line you added
# sudo sed -i '/myapp.local/d' /etc/hosts
```

**Production use:** `/etc/hosts` overrides DNS. In development, you add entries to test with real-looking domain names.

### Exercise 2.B.9 — Check Open Connections

```bash
# List all established TCP connections
ss -tnp

# Count connections per state
ss -s

# Show all connections to a specific remote
ss -tnp | grep "google" || echo "No active connections to Google"
```

### Exercise 2.B.10 — Download Files

```bash
# Download with curl
curl -o /tmp/test_download.txt http://httpbin.org/robots.txt

# Download with wget (if available)
wget -O /tmp/test_download2.txt http://httpbin.org/robots.txt 2>/dev/null || echo "wget not available"

# Verify
cat /tmp/test_download.txt

# Clean up
rm -f /tmp/test_download.txt /tmp/test_download2.txt
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 2.C.1 — Run a Python HTTP Server and Inspect Traffic

```bash
# Start a simple HTTP server
cd /tmp/linux-lab
python3 -m http.server 8888 &
HTTP_PID=$!

sleep 1

# Verify it's listening
ss -tlnp | grep 8888

# Make requests
curl -s http://localhost:8888/ | head -5
curl -s http://localhost:8888/logs/ | head -5

# Check access from different addresses
curl -s http://127.0.0.1:8888/ > /dev/null && echo "127.0.0.1 works"

# Show the server's connections
ss -tnp | grep 8888

# Clean up
kill $HTTP_PID
```

### Exercise 2.C.2 — Understand Connection Refused vs Timeout

```bash
# Connection REFUSED — port exists but nothing is listening
curl -s --connect-timeout 3 http://localhost:9999/ 2>&1
# Expected: Connection refused (immediate response)

# Connection TIMEOUT — simulate by dropping packets (if iptables available)
# sudo iptables -A INPUT -p tcp --dport 9998 -j DROP
# curl --connect-timeout 3 http://localhost:9998/
# Expected: Connection timed out (waits 3 seconds)
# sudo iptables -D INPUT -p tcp --dport 9998 -j DROP

echo "Connection refused = port unreachable, nothing listening"
echo "Connection timeout = packets being dropped (firewall/network issue)"
```

### Exercise 2.C.3 — The `0.0.0.0` vs `127.0.0.1` Experiment

```bash
# Start server bound to 127.0.0.1
python3 -c "
from http.server import HTTPServer, SimpleHTTPRequestHandler
server = HTTPServer(('127.0.0.1', 8881), SimpleHTTPRequestHandler)
print('Listening on 127.0.0.1:8881')
server.serve_forever()
" &
PID1=$!

# Start another server bound to 0.0.0.0
python3 -c "
from http.server import HTTPServer, SimpleHTTPRequestHandler
server = HTTPServer(('0.0.0.0', 8882), SimpleHTTPRequestHandler)
print('Listening on 0.0.0.0:8882')
server.serve_forever()
" &
PID2=$!

sleep 1

# Check what's listening
ss -tlnp | grep -E "888[12]"

# From local machine, both work
curl -s -o /dev/null -w "%{http_code}" http://localhost:8881
curl -s -o /dev/null -w "%{http_code}" http://localhost:8882

# From another machine (if you have one), only 8882 would be reachable
# Get your actual IP
MY_IP=$(hostname -I | awk '{print $1}')
echo "Try from another machine:"
echo "  curl http://$MY_IP:8881  → will FAIL (bound to 127.0.0.1)"
echo "  curl http://$MY_IP:8882  → will WORK (bound to 0.0.0.0)"

# Clean up
kill $PID1 $PID2
```

### Exercise 2.C.4 — DNS Failure Simulation

```bash
# Check current DNS
cat /etc/resolv.conf

# Test normal resolution
nslookup google.com && echo "DNS works"

# Simulate DNS failure (use a nonexistent DNS server)
# Be careful — this temporarily breaks name resolution
# (Only do this if you can restore /etc/resolv.conf)

# Instead, test with a nonexistent domain
nslookup this.domain.does.not.exist.invalid 2>&1
# Expected: ** server can't find ...

# Test how curl behaves with DNS failure
curl --connect-timeout 3 http://this.domain.does.not.exist.invalid/ 2>&1
# Expected: Could not resolve host
```

### Exercise 2.C.5 — HTTP Headers Deep Dive

```bash
# Send custom headers
curl -v -H "Authorization: Bearer token123" \
     -H "X-Request-ID: abc-def" \
     http://httpbin.org/headers

# See what headers the server sends back
curl -sI http://httpbin.org/get

# Common important headers:
# Content-Type: what format the body is in
# Authorization: authentication credentials
# X-Request-ID: trace a request across services
# Cache-Control: caching behavior
# Content-Length: size of the response body
```

### Exercise 2.C.6 — Port Scanning (Your Own Machine Only)

```bash
# Check which ports are open on localhost
# Method 1: ss
ss -tlnp | awk 'NR>1 {print $4}' | sort -t: -k2 -n

# Method 2: bash built-in (check specific ports)
for port in 22 80 443 3000 5432 8000 8080 8888; do
    (echo > /dev/tcp/localhost/$port) 2>/dev/null && echo "Port $port: OPEN" || echo "Port $port: CLOSED"
done
```

### Exercise 2.C.7 — Measure Latency to Different Endpoints

```bash
# Local latency (sub-millisecond)
ping -c 5 127.0.0.1

# Gateway latency (usually <1ms)
GATEWAY=$(ip route | grep default | awk '{print $3}')
ping -c 5 "$GATEWAY" 2>/dev/null || echo "No default gateway (container?)"

# Internet latency
ping -c 5 8.8.8.8

# Compare:
echo "=== Latency Summary ==="
echo "Loopback:  ~0.01ms (memory copy)"
echo "LAN:       ~0.5ms (local network)"
echo "Internet:  ~10-100ms (depends on distance)"
```

### Exercise 2.C.8 — TCP Connection States

```bash
# Start a server
python3 -m http.server 8877 &
HTTP_PID=$!
sleep 1

# Make several connections
for i in $(seq 1 5); do
    curl -s http://localhost:8877/ > /dev/null &
done
sleep 1

# Inspect connection states
ss -tn | head -20

# Count connections by state
ss -s

# Common states:
# ESTABLISHED — active data transfer
# TIME_WAIT   — connection closed, waiting for stale packets to expire
# CLOSE_WAIT  — remote closed, local hasn't closed yet (often a bug)
# LISTEN      — waiting for new connections

kill $HTTP_PID
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 2.D.1 — Debug: "Connection Refused" on Working Service

**Scenario:** FastAPI is running. `curl http://localhost:8000` works. But another machine can't connect.

**Root cause candidates:**
1. App is bound to `127.0.0.1` instead of `0.0.0.0`
2. Firewall is blocking the port
3. The other machine is using the wrong IP

**Diagnosis:**
```bash
# Step 1: Check what address the app is bound to
ss -tlnp | grep 8000
# If it shows 127.0.0.1:8000 → that's your problem
# Should show 0.0.0.0:8000 or *:8000

# Step 2: Check firewall
sudo iptables -L -n 2>/dev/null | grep 8000
sudo ufw status 2>/dev/null

# Step 3: Verify the correct IP
hostname -I
```

**Fix:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
# NOT: uvicorn app:app --host 127.0.0.1 --port 8000
```

### Exercise 2.D.2 — Debug: curl Inside Docker Container Fails

**Scenario:** You have a Docker container running. You exec into it and try `curl http://host-service:8000` but get `Could not resolve host`.

**Diagnosis:**
```bash
# Inside the container:
cat /etc/resolv.conf
# Docker uses 127.0.0.11 as DNS

# Try by IP instead of hostname
curl http://172.17.0.1:8000  # Docker bridge gateway (host machine)

# Check if the hostname is defined
cat /etc/hosts

# From host, check Docker network
docker network ls
docker network inspect bridge
```

**Root causes:**
1. The hostname isn't resolvable — use `docker-compose` services or `--network` for automatic DNS
2. The host service is bound to `127.0.0.1` — not reachable from Docker's network namespace
3. Docker's internal DNS doesn't know about host machine services

### Exercise 2.D.3 — Debug: Intermittent "Connection Reset"

**Scenario:** Requests to your service occasionally fail with `Connection reset by peer`.

**Simulation:**
```bash
# Create a server that randomly kills connections
cat > /tmp/flaky_server.py <<'EOF'
import socket
import random
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8765))
server.listen(5)
print("Flaky server listening on 8765")

while True:
    conn, addr = server.accept()
    if random.random() < 0.5:
        # Simulate crash: close without sending response
        conn.close()
        print(f"DROPPED connection from {addr}")
    else:
        response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"
        conn.sendall(response.encode())
        conn.close()
        print(f"OK response to {addr}")
EOF

python3 /tmp/flaky_server.py &
FLAKY_PID=$!
sleep 1

# Send 10 requests
for i in $(seq 1 10); do
    RESULT=$(curl -s --connect-timeout 2 http://localhost:8765/ 2>&1)
    echo "Request $i: $RESULT"
done

kill $FLAKY_PID
rm /tmp/flaky_server.py
```

**Production root causes for connection reset:**
- Server crash/OOM during response
- Proxy timeout (nginx kills the upstream connection)
- Keep-alive mismatch (server closes idle connection while client reuses it)
- TLS renegotiation failure

### Exercise 2.D.4 — Debug: DNS Works but HTTPS Fails

**Scenario:** `nslookup myservice.com` resolves, but `curl https://myservice.com` fails with certificate error.

```bash
# Check DNS
nslookup httpbin.org

# Test HTTPS
curl -v https://httpbin.org 2>&1 | grep -E "SSL|certificate|error"

# Common SSL errors:
# "SSL certificate problem: self-signed certificate" → The server uses a self-signed cert
# "SSL certificate problem: certificate has expired" → Cert not renewed
# "SSL: no alternative certificate subject name matches" → Cert doesn't match hostname

# Skip cert verification (DANGEROUS — debug only)
curl -k https://self-signed.badssl.com/

# Show certificate details
echo | openssl s_client -connect httpbin.org:443 2>/dev/null | openssl x509 -text -noout | head -20
```

### Exercise 2.D.5 — Debug: TIME_WAIT Exhaustion

**Scenario:** Under heavy load, new connections start failing. You see thousands of TIME_WAIT connections.

```bash
# Count connections by state
ss -s

# Count TIME_WAIT specifically
ss -tn state time-wait | wc -l

# Check TIME_WAIT connections per destination
ss -tn state time-wait | awk '{print $4}' | sort | uniq -c | sort -rn | head -10

# Check kernel parameters
cat /proc/sys/net/ipv4/tcp_fin_timeout  # Default: 60 seconds
cat /proc/sys/net/ipv4/tcp_tw_reuse     # 0 = disabled

# Fix (temporary):
# sudo sysctl -w net.ipv4.tcp_tw_reuse=1
# Fix (permanent): add to /etc/sysctl.conf
```

**Why TIME_WAIT exists:** After closing a connection, the OS keeps the socket entry for 60 seconds to handle any delayed packets from the old connection. Under heavy load with short-lived connections (like HTTP requests to a database), you can run out of available local ports.

### Exercise 2.D.6 — Debug: Docker Port Mapping Not Working

**Scenario:** Docker runs with `-p 8000:8000` but `curl http://localhost:8000` returns `Connection refused`.

**Diagnostic checklist:**

```bash
# 1. Is the container running?
docker ps | grep your-container

# 2. Is the app actually listening inside the container?
docker exec your-container ss -tlnp
# If it shows 127.0.0.1:8000 → that's the bug. Must be 0.0.0.0:8000

# 3. Check Docker port mapping
docker port your-container

# 4. Check Docker logs
docker logs your-container | tail -20

# 5. Check if Docker itself is listening
ss -tlnp | grep 8000
# Should show dockerd or docker-proxy

# 6. Test from inside the container
docker exec your-container curl http://localhost:8000/health
```

**Most common fix:** Change `--host 127.0.0.1` to `--host 0.0.0.0` in your uvicorn command.

### Exercise 2.D.7 — Debug: Slow Response Times

```bash
# Create a server with artificial latency
cat > /tmp/slow_server.py <<'EOF'
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

class SlowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/slow":
            time.sleep(5)  # Simulated slow database query
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    
    def log_message(self, format, *args):
        pass  # Suppress logs

server = HTTPServer(('0.0.0.0', 8766), SlowHandler)
print("Slow server on 8766")
server.serve_forever()
EOF

python3 /tmp/slow_server.py &
SLOW_PID=$!
sleep 1

# Measure response times
echo "=== Fast endpoint ==="
curl -w "Total: %{time_total}s\n" -s -o /dev/null http://localhost:8766/

echo "=== Slow endpoint ==="
curl -w "Total: %{time_total}s\n" -s -o /dev/null http://localhost:8766/slow

# With timeout to catch hanging requests
curl --max-time 3 http://localhost:8766/slow 2>&1 || echo "TIMEOUT after 3s"

kill $SLOW_PID
rm /tmp/slow_server.py
```

**Production insight:** Configure client timeouts (`--max-time`, `--connect-timeout`). Server-side, use async handlers so one slow request doesn't block everything.

### Exercise 2.D.8 — Full Network Diagnostic Script

```bash
cat > /tmp/net_diagnose.sh <<'SCRIPT'
#!/bin/bash
set -uo pipefail

TARGET_HOST="${1:-localhost}"
TARGET_PORT="${2:-8000}"

echo "============================================"
echo "  NETWORK DIAGNOSTIC: $TARGET_HOST:$TARGET_PORT"
echo "  $(date)"
echo "============================================"

# 1. DNS Resolution
echo -e "\n[1] DNS Resolution"
if [[ "$TARGET_HOST" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "  IP address provided, skipping DNS"
else
    nslookup "$TARGET_HOST" 2>/dev/null && echo "  ✓ DNS resolves" || echo "  ✗ DNS FAILED"
fi

# 2. Ping test
echo -e "\n[2] Ping Test"
ping -c 2 -W 2 "$TARGET_HOST" > /dev/null 2>&1 && echo "  ✓ Host reachable" || echo "  ⚠ Ping failed (may be blocked)"

# 3. TCP Connection
echo -e "\n[3] TCP Connection Test"
(echo > /dev/tcp/"$TARGET_HOST"/"$TARGET_PORT") 2>/dev/null \
    && echo "  ✓ Port $TARGET_PORT is OPEN" \
    || echo "  ✗ Port $TARGET_PORT is CLOSED/FILTERED"

# 4. HTTP Test (if applicable)
echo -e "\n[4] HTTP Test"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "http://$TARGET_HOST:$TARGET_PORT/" 2>/dev/null)
if [[ "$HTTP_CODE" -gt 0 ]]; then
    echo "  HTTP Status: $HTTP_CODE"
else
    echo "  ✗ HTTP connection failed"
fi

# 5. Timing
echo -e "\n[5] Response Timing"
curl -w "  DNS: %{time_namelookup}s | Connect: %{time_connect}s | Total: %{time_total}s\n" \
     -s -o /dev/null --connect-timeout 3 "http://$TARGET_HOST:$TARGET_PORT/" 2>/dev/null || echo "  ✗ Timing unavailable"

# 6. Local port status
echo -e "\n[6] Local Listening Check"
ss -tlnp 2>/dev/null | grep ":$TARGET_PORT " || echo "  Nothing listening on port $TARGET_PORT locally"

echo -e "\n============================================"
echo "  DIAGNOSTIC COMPLETE"
echo "============================================"
SCRIPT
chmod +x /tmp/net_diagnose.sh

# Test it
/tmp/net_diagnose.sh localhost 22
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Multi-Service Communication Debugging

**Situation:** You have a three-tier application:
- **Frontend** on port 3000
- **API** (FastAPI) on port 8000
- **Database** on port 5432

The API can reach the database, but the frontend can't reach the API. Users report "Network Error."

**Your diagnostic workflow:**

```bash
# Step 1: Is the API process running?
ps aux | grep uvicorn
ss -tlnp | grep 8000

# Step 2: What address is it bound to?
ss -tlnp | grep 8000
# If 127.0.0.1:8000 → frontend (running in browser/different host) can't reach it

# Step 3: Can you reach it locally?
curl http://localhost:8000/health

# Step 4: Can you reach it by IP?
curl http://$(hostname -I | awk '{print $1}'):8000/health

# Step 5: Is there a proxy in front (nginx)?
ss -tlnp | grep -E "80|443"
# Check nginx config for upstream pointing to wrong port

# Step 6: Check CORS headers (browser-specific)
curl -v -X OPTIONS http://localhost:8000/ \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" 2>&1 | grep "Access-Control"

# Step 7: Check firewall
sudo iptables -L -n 2>/dev/null | head -20
```

**Acceptance Criteria:**
- [ ] Correctly identify which layer is failing
- [ ] Distinguish between DNS, TCP, HTTP, and application-layer failures
- [ ] Know when it's a `127.0.0.1` vs `0.0.0.0` issue
- [ ] Know when it's a firewall issue
- [ ] Know when it's a CORS issue (browser) vs a real network issue

**Validation Checklist:**
- [ ] Can explain the difference between `Connection refused` and `Connection timed out`
- [ ] Can use `ss -tlnp` to find what's listening on a port
- [ ] Can use `curl -v` to see full HTTP exchange
- [ ] Can use `curl -w` to measure latency at each phase
- [ ] Can diagnose Docker networking issues (host vs bridge)

---

## Key Takeaways

1. **`0.0.0.0` vs `127.0.0.1`** is the single most important networking concept for Developers
2. **Connection refused ≠ firewall.** Refused means nothing is listening. Timeout means firewall/network.
3. **DNS is a separate layer.** If `nslookup` works but `curl` doesn't, it's not DNS.
4. **Every layer has its own failure mode:** DNS → TCP → TLS → HTTP → Application
5. **Docker networking is a different universe.** Containers have their own IP, DNS, and routing.
6. **Always bind to `0.0.0.0` inside containers.** Always.

---

*Next: [Section 4 — Database Fundamentals](04-database-fundamentals.md)*
