# SECTION 1 — LINUX THEORY & LAB

---

## PART A — CONCEPT EXPLANATION

### What is a Process?

A **process** is a running instance of a program. When you type `python app.py`, the kernel:

1. Allocates memory for the program
2. Loads the binary into memory
3. Assigns a **PID** (Process ID) — a unique integer
4. Creates an entry in the **process table**
5. Starts executing instructions

Every process has:
- **PID** — unique identifier
- **PPID** — parent process ID (every process has a parent, except `init`/`systemd` with PID 1)
- **UID** — the user who owns the process
- **State** — running, sleeping, stopped, zombie
- **File descriptors** — stdin (0), stdout (1), stderr (2), and any open files/sockets

**Mental model:** Think of processes as rows in a spreadsheet. The kernel manages the spreadsheet. `ps` lets you read it. `kill` lets you delete rows.

**How it breaks in production:**
- A process that doesn't exit becomes a zombie (entry in the table, consuming a PID slot)
- A process that forks endlessly causes a **fork bomb** (`:(){ :|:& };:`)
- If you start uvicorn without `&` or a process manager, closing your SSH session kills the server

### What is a Port?

A **port** is a 16-bit number (0–65535) that identifies a specific service on a machine. When a client connects to `192.168.1.50:8000`, the OS routes the connection to whichever process is **listening** on port 8000.

**Port ranges:**
- **0–1023** — well-known (privileged), require root: HTTP (80), HTTPS (443), SSH (22)
- **1024–49151** — registered: PostgreSQL (5432), Redis (6379)
- **49152–65535** — dynamic/ephemeral, used for outgoing connections

**What happens when two processes try to listen on the same port?** The second one fails with `Address already in use`. This is the #1 reason `uvicorn` won't start.

**Production lesson:** Always check `ss -tulnp` before starting a service. If port 8000 is busy, find and kill the old process.

### What is a File Permission?

In Linux, **everything is a file** — regular files, directories, devices, sockets. Each file has:

```
-rwxr-xr-- 1 arun devteam 4096 Feb 17 09:00 script.sh
 │││ │││ │││
 │││ │││ └── Others: read only
 │││ └──── Group: read + execute
 └────── Owner: read + write + execute
```

**Three permission sets** (owner, group, others) × **three permissions** (read, write, execute) = 9 bits.

**Numeric notation:**
- `r=4`, `w=2`, `x=1`
- `rwxr-xr--` = `754`
- `chmod 755 file` = owner rwx, group rx, others rx

**What trips beginners:**
- A script won't run? You forgot `chmod +x script.sh`
- A file is readable but the directory isn't executable? You can't `ls` or `cd` into it
- `Permission denied` on a Docker socket? Your user isn't in the `docker` group

### What is a Shell?

A **shell** is a program that reads commands, interprets them, and asks the kernel to execute them. It's the **interface between you and the operating system**.

Common shells:
- **bash** — Bourne Again Shell, the default on most Linux/macOS systems
- **zsh** — Z Shell, default on modern macOS, more features
- **sh** — POSIX shell, minimal, used in scripts for portability

**What happens when you type `ls -la`:**
1. Shell reads the line
2. Splits it: command = `ls`, args = `["-la"]`
3. Searches `$PATH` for `ls` binary (e.g., `/usr/bin/ls`)
4. Calls `fork()` to create a child process
5. Calls `exec()` to replace the child with `ls`
6. `ls` runs, writes to stdout
7. Shell waits for `ls` to finish (`wait()`), then shows the next prompt

**Environment variables** live per-process. `export FOO=bar` adds `FOO` to the current shell's environment, and all child processes inherit it.

### What is a Daemon?

A **daemon** is a background process that runs continuously without a terminal. Examples:
- `sshd` — SSH server daemon
- `dockerd` — Docker daemon
- `systemd` — the init system itself

Daemons are typically:
- Started at boot via `systemd` service files
- Detached from any terminal
- Log to syslog or journal instead of stdout
- Managed with `systemctl start|stop|restart|status <service>`

**When you run `uvicorn &`**, it's *not* a proper daemon — it's a background process tied to your shell session. When you log out, it dies (unless you use `nohup` or `tmux`).

### What Happens When You Run a Command?

```
You type: python app.py

1. Bash reads the input
2. Bash searches $PATH for "python" → /usr/bin/python (or .venv/bin/python)
3. Bash calls fork() → creates child process (copy of bash)
4. Child calls execve("/usr/bin/python", ["python", "app.py"], environ)
   → Kernel loads Python interpreter into memory
5. Python interpreter reads app.py
6. Python executes the bytecode
7. If app.py starts a web server → Python keeps running, listening on a socket
8. When Python exits → kernel cleans up the process
9. Bash wakes up (was in wait()) → shows prompt again
```

**Key insight:** *Every command you type goes through this cycle.* The shell is just a loop: read → parse → fork → exec → wait → repeat.

### Common Beginner Misunderstandings

| Mistake | Reality |
|---|---|
| "I deleted a file so it's gone" | If a process has the file open, it still exists on disk until the process closes it |
| "I ran `export VAR=x` and it persists" | Environment variables die with the shell session. Put them in `.bashrc` or `.env` |
| "root can do everything safely" | root can `rm -rf /` and destroy the system. Use `sudo` sparingly |
| "Ctrl+C kills the process" | It sends SIGINT. The process can catch and ignore it. Use `kill -9` for unkillable processes |
| "Closing the terminal stops background jobs" | It sends SIGHUP. Use `nohup`, `tmux`, or `systemd` for persistence |

---

## PART B — BEGINNER PRACTICE (20 Exercises)

### Exercise 1.B.1 — Navigate the Filesystem

```bash
# Print current directory
pwd

# List files with details
ls -la

# List files by modification time
ls -lt

# Go to home directory
cd ~

# Go to the project
cd ~/Projects/production-engineering-lab

# Go up one level
cd ..

# Go back to previous directory
cd -
```

**Expected:** You should see different output at each step. `cd -` takes you to the last directory you were in.

### Exercise 1.B.2 — Create a Directory Tree

```bash
mkdir -p /tmp/linux-lab/{logs,data,config,scripts}
ls -R /tmp/linux-lab/
```

**Expected:**
```
/tmp/linux-lab/:
config  data  logs  scripts
```

**Note:** `-p` creates parent directories as needed and doesn't error if they exist.

### Exercise 1.B.3 — Create and Manipulate Files

```bash
cd /tmp/linux-lab

# Create files
echo "Hello World" > data/greeting.txt
echo "Error occurred" > logs/error.log
echo "DEBUG: testing" >> logs/error.log

# Read files
cat data/greeting.txt
cat logs/error.log
```

**Key:** `>` overwrites, `>>` appends. This is the #1 distinction beginners confuse.

### Exercise 1.B.4 — Copy, Move, Remove

```bash
# Copy a file
cp data/greeting.txt data/greeting_backup.txt

# Copy a directory recursively
cp -r data/ data_backup/

# Move/rename a file
mv data/greeting_backup.txt data/old_greeting.txt

# Remove a file
rm data/old_greeting.txt

# Remove a directory recursively (DANGEROUS with wrong path)
rm -rf data_backup/

# Verify
ls -R
```

**WARNING:** `rm -rf` has no undo. Always double-check the path. Never run `rm -rf /` or `rm -rf ~`.

### Exercise 1.B.5 — Search File Contents with grep

```bash
# Create a sample log file
cat > logs/app.log <<'EOF'
2026-02-17 10:00:01 INFO  Server started on port 8000
2026-02-17 10:00:05 INFO  Request: GET /health → 200
2026-02-17 10:00:10 ERROR Connection refused: database unreachable
2026-02-17 10:01:00 WARN  Slow response: 2500ms for /predict
2026-02-17 10:01:05 INFO  Request: POST /predict → 200
2026-02-17 10:02:00 ERROR Timeout: upstream service did not respond
2026-02-17 10:03:00 INFO  Request: GET /metrics → 200
EOF

# Search for errors
grep "ERROR" logs/app.log

# Case-insensitive search
grep -i "error" logs/app.log

# Show line numbers
grep -n "ERROR" logs/app.log

# Count matches
grep -c "ERROR" logs/app.log

# Invert match (show non-error lines)
grep -v "ERROR" logs/app.log

# Search recursively in all files
grep -r "ERROR" logs/
```

**Expected:** 2 ERROR lines. Understand `-n`, `-c`, `-v`, `-r` — you'll use these daily.

### Exercise 1.B.6 — Find Files

```bash
# Find all .log files
find /tmp/linux-lab -name "*.log"

# Find files modified in last 10 minutes
find /tmp/linux-lab -mmin -10

# Find files larger than 0 bytes
find /tmp/linux-lab -size +0c -type f

# Find and execute a command on results
find /tmp/linux-lab -name "*.log" -exec wc -l {} \;
```

### Exercise 1.B.7 — Understand File Permissions

```bash
# Create a script
cat > scripts/deploy.sh <<'EOF'
#!/bin/bash
echo "Deploying application..."
echo "Done."
EOF

# Check permissions
ls -l scripts/deploy.sh

# Try to run it (will fail)
./scripts/deploy.sh

# Make it executable
chmod +x scripts/deploy.sh

# Run it again (now works)
./scripts/deploy.sh

# Understand numeric permissions
stat -c "%a %n" scripts/deploy.sh
```

**Expected:** First run fails with `Permission denied`. After `chmod +x`, it works.

### Exercise 1.B.8 — Process Management Basics

```bash
# Start a background process
sleep 300 &

# See the background job
jobs

# List your processes
ps aux | grep sleep

# Get just the PID
pgrep sleep

# Kill it
kill $(pgrep -f "sleep 300")

# Verify it's gone
ps aux | grep sleep
```

### Exercise 1.B.9 — Monitor System Resources

```bash
# Quick process overview (press q to quit)
top -bn1 | head -20

# Memory usage
free -h

# Disk usage
df -h

# Directory size
du -sh /tmp/linux-lab/
```

### Exercise 1.B.10 — I/O Redirection and Pipes

```bash
# Redirect stdout to file
ls -la > /tmp/linux-lab/filelist.txt

# Redirect stderr to file
ls /nonexistent 2> /tmp/linux-lab/error.txt

# Redirect both
ls -la /tmp/linux-lab /nonexistent > /tmp/linux-lab/all.txt 2>&1

# Pipe to another command
cat logs/app.log | grep ERROR | wc -l

# Pipe to sort
du -sh /tmp/linux-lab/* | sort -h
```

### Exercise 1.B.11 — Environment Variables

```bash
# Set a variable (local to this shell)
MY_VAR="hello"
echo $MY_VAR

# Export it (available to child processes)
export APP_PORT=8000
echo $APP_PORT

# Use in a command
echo "Server will run on port $APP_PORT"

# See all environment variables
env | head -20

# Unset
unset APP_PORT
echo $APP_PORT  # empty
```

### Exercise 1.B.12 — Viewing Files (head, tail, less)

```bash
# First 5 lines
head -5 logs/app.log

# Last 3 lines
tail -3 logs/app.log

# Follow a log file in real-time (Ctrl+C to stop)
tail -f logs/app.log &
echo "2026-02-17 10:04:00 INFO  New entry" >> logs/app.log
kill %1
```

**`tail -f`** is the most important log debugging tool. It shows new lines as they're written.

### Exercise 1.B.13 — Archiving and Compression

```bash
# Create a tar archive
tar -cvf /tmp/lab-backup.tar /tmp/linux-lab/

# Create compressed archive
tar -czvf /tmp/lab-backup.tar.gz /tmp/linux-lab/

# List contents without extracting
tar -tzvf /tmp/lab-backup.tar.gz

# Extract
mkdir /tmp/restored
tar -xzvf /tmp/lab-backup.tar.gz -C /tmp/restored/

# Clean up
rm -rf /tmp/lab-backup.tar /tmp/lab-backup.tar.gz /tmp/restored
```

### Exercise 1.B.14 — Text Processing with awk and cut

```bash
# Extract the timestamp and level from logs
awk '{print $1, $2, $3}' logs/app.log

# Extract only ERROR lines and show the message
awk '/ERROR/ {$1=$2=$3=""; print $0}' logs/app.log

# Cut: extract fields by delimiter
echo "user:password:1000:1000::/home/user:/bin/bash" | cut -d: -f1,3

# Count requests per status code
grep "→" logs/app.log | awk '{print $NF}' | sort | uniq -c | sort -rn
```

### Exercise 1.B.15 — Working with which, type, and command -v

```bash
# Find where a command lives
which python3
which bash
which uv

# More detail with type
type ls
type cd      # cd is a shell builtin — no binary
type python3

# Check if command exists (useful in scripts)
command -v docker && echo "Docker is installed" || echo "Docker not found"
```

### Exercise 1.B.16 — Symbolic Links

```bash
# Create a symlink
ln -s /tmp/linux-lab/logs/app.log /tmp/linux-lab/latest.log

# Verify
ls -la /tmp/linux-lab/latest.log  # shows -> target

# Read via symlink
cat /tmp/linux-lab/latest.log

# Remove symlink (doesn't remove target)
rm /tmp/linux-lab/latest.log
cat /tmp/linux-lab/logs/app.log  # still exists
```

**Production use:** `/var/log/app/current` → symlink to today's log file.

### Exercise 1.B.17 — History and Shortcuts

```bash
# Show command history
history | tail -20

# Search history (Ctrl+R, then type)
# Press Ctrl+R and type "grep" — bash finds your last grep command

# Repeat last command
!!

# Repeat last command starting with "find"
!find

# Use last argument of previous command
echo "some file.txt"
cat !$  # uses "some file.txt"
```

### Exercise 1.B.18 — xargs for Batch Operations

```bash
# Find all .log files and count their lines
find /tmp/linux-lab -name "*.log" | xargs wc -l

# Delete all empty files
find /tmp/linux-lab -empty -type f | xargs rm -v

# Run a command for each result
echo -e "file1\nfile2\nfile3" | xargs -I {} touch /tmp/linux-lab/data/{}
ls /tmp/linux-lab/data/
```

### Exercise 1.B.19 — Watch and Repeat Commands

```bash
# Run a command every 2 seconds (Ctrl+C to stop)
watch -n 2 "ps aux | grep python | grep -v grep"

# (In another terminal, start and stop a python process to see it appear/disappear)
```

### Exercise 1.B.20 — The PATH Variable

```bash
# Show your PATH
echo $PATH | tr ':' '\n'

# Create a custom script
mkdir -p ~/bin
cat > ~/bin/greet <<'EOF'
#!/bin/bash
echo "Hello, $(whoami)! Today is $(date +%A)."
EOF
chmod +x ~/bin/greet

# Add ~/bin to PATH (for this session)
export PATH="$HOME/bin:$PATH"

# Now run it from anywhere
greet
```

---

## PART C — INTERMEDIATE PRACTICE (20 Exercises)

### Exercise 1.C.1 — Process Tree Investigation

```bash
# Start a chain of processes
bash -c 'bash -c "sleep 600"' &

# Show the process tree
pstree -p $$

# Find the sleep process and its parents
ps -ef | grep sleep
ps -p <PID> -o pid,ppid,cmd

# Kill the parent bash — what happens to sleep?
kill <parent_bash_pid>
ps aux | grep sleep  # Is sleep still running? (Yes — it gets reparented to PID 1)
```

**Lesson:** When a parent process dies, children are adopted by `init`/`systemd` (PID 1). They become **orphan processes**.

### Exercise 1.C.2 — Zombie Process Creation

```bash
# Create a zombie process
cat > /tmp/zombie.py <<'EOF'
import os, time
pid = os.fork()
if pid > 0:
    # Parent: sleep without calling wait()
    print(f"Parent PID: {os.getpid()}, Child PID: {pid}")
    time.sleep(60)  # Child finishes but parent never reaps it
else:
    # Child: exit immediately
    print(f"Child exiting: PID {os.getpid()}")
    os._exit(0)
EOF

python3 /tmp/zombie.py &

# After a second, check for zombies
ps aux | grep Z
# Look for a process in state "Z" (zombie)

# Kill the parent to clean up
kill %1
```

**Why zombies matter:** Each zombie occupies a PID slot. Too many → the system can't create new processes.

### Exercise 1.C.3 — Signal Handling

```bash
# Create a signal-handling script
cat > /tmp/signal_test.sh <<'EOF'
#!/bin/bash
trap 'echo "Caught SIGINT (Ctrl+C) — ignoring"' INT
trap 'echo "Caught SIGTERM — cleaning up..."; exit 0' TERM
echo "PID: $$. Try Ctrl+C, then kill me with SIGTERM."
while true; do sleep 1; done
EOF
chmod +x /tmp/signal_test.sh

# Run it
/tmp/signal_test.sh &
SIGNAL_PID=$!

# Try SIGINT (process catches and ignores)
kill -INT $SIGNAL_PID

# Try SIGTERM (process catches, cleans up, exits)
kill -TERM $SIGNAL_PID

# If all else fails, SIGKILL cannot be caught
# kill -9 $SIGNAL_PID
```

**Production lesson:** Your FastAPI server receives SIGTERM during deployment. If it doesn't handle it, in-flight requests get dropped.

### Exercise 1.C.4 — File Descriptor Investigation

```bash
# Start a Python process that opens files
python3 -c "
import time
f1 = open('/tmp/fd_test1.txt', 'w')
f2 = open('/tmp/fd_test2.txt', 'w')
f1.write('hello')
print(f'PID: {__import__(\"os\").getpid()}')
time.sleep(120)
" &

FD_PID=$!
sleep 1

# List open file descriptors
ls -la /proc/$FD_PID/fd/

# Count open files
ls /proc/$FD_PID/fd/ | wc -l

# Kill the process
kill $FD_PID
```

**What you'll see:** FD 0 (stdin), 1 (stdout), 2 (stderr), plus the two files you opened.

### Exercise 1.C.5 — Disk Space Forensics

```bash
# Create a large file
dd if=/dev/zero of=/tmp/linux-lab/largefile.bin bs=1M count=100

# Check disk usage
df -h /tmp
du -sh /tmp/linux-lab/*

# Find the biggest files
find /tmp/linux-lab -type f -exec du -h {} \; | sort -rh | head -5

# Clean up
rm /tmp/linux-lab/largefile.bin
```

### Exercise 1.C.6 — Log Analysis Pipeline

```bash
# Create a realistic access log
cat > /tmp/linux-lab/logs/access.log <<'EOF'
192.168.1.10 - - [17/Feb/2026:10:00:01] "GET /health HTTP/1.1" 200 15
192.168.1.11 - - [17/Feb/2026:10:00:02] "POST /predict HTTP/1.1" 200 1234
192.168.1.10 - - [17/Feb/2026:10:00:03] "GET /health HTTP/1.1" 200 15
192.168.1.12 - - [17/Feb/2026:10:00:04] "POST /predict HTTP/1.1" 500 89
192.168.1.10 - - [17/Feb/2026:10:00:05] "GET /metrics HTTP/1.1" 200 4567
192.168.1.13 - - [17/Feb/2026:10:00:06] "POST /predict HTTP/1.1" 200 1234
192.168.1.12 - - [17/Feb/2026:10:00:07] "POST /predict HTTP/1.1" 500 89
192.168.1.14 - - [17/Feb/2026:10:00:08] "GET /health HTTP/1.1" 200 15
192.168.1.12 - - [17/Feb/2026:10:00:09] "POST /predict HTTP/1.1" 200 1234
192.168.1.15 - - [17/Feb/2026:10:00:10] "DELETE /predict HTTP/1.1" 405 50
EOF

# Count requests per status code
awk '{print $(NF-1)}' /tmp/linux-lab/logs/access.log | sort | uniq -c | sort -rn

# Find unique IPs
awk '{print $1}' /tmp/linux-lab/logs/access.log | sort -u

# Count requests per IP
awk '{print $1}' /tmp/linux-lab/logs/access.log | sort | uniq -c | sort -rn

# Find all 500 errors
grep '" 500 ' /tmp/linux-lab/logs/access.log

# Extract just the endpoints
awk -F'"' '{print $2}' /tmp/linux-lab/logs/access.log | awk '{print $2}' | sort | uniq -c | sort -rn
```

### Exercise 1.C.7 — Process Resource Limits

```bash
# Check current limits
ulimit -a

# Check max open files
ulimit -n

# Try to create more file descriptors than allowed
python3 -c "
import os, sys
files = []
try:
    for i in range(10000):
        files.append(open(f'/tmp/fd_test_{i}', 'w'))
except OSError as e:
    print(f'Failed at {len(files)} files: {e}')
finally:
    for f in files:
        f.close()
    for i in range(len(files)):
        os.remove(f'/tmp/fd_test_{i}')
"
```

**Production lesson:** Default `ulimit -n` is often 1024. A busy web server can easily exceed this. Production deployments increase it to 65536+.

### Exercise 1.C.8 — Background Jobs and Job Control

```bash
# Start multiple background jobs
sleep 100 &
sleep 200 &
sleep 300 &

# List all jobs
jobs -l

# Bring a job to foreground
fg %2

# Suspend it (Ctrl+Z)
# Then send it back to background
bg %2

# Kill a specific job
kill %3

# Kill all jobs
kill $(jobs -p)
```

### Exercise 1.C.9 — Using screen or tmux for Persistent Sessions

```bash
# Start a new tmux session (if tmux is available)
tmux new-session -d -s lab "bash"

# List sessions
tmux list-sessions

# Attach to the session
tmux attach-session -t lab

# Inside tmux: run a long command
# (press Ctrl+B, then D to detach — the command keeps running)

# Kill the session
tmux kill-session -t lab
```

**Production lesson:** Always use tmux/screen when running long operations over SSH. If your connection drops, the process survives.

### Exercise 1.C.10 — Cron Jobs (Scheduled Tasks)

```bash
# List current cron jobs
crontab -l 2>/dev/null || echo "No crontab set"

# Create a cron job (write to a temp file, then install)
cat > /tmp/my_cron <<'EOF'
# Run every 5 minutes: check if app is alive
*/5 * * * * curl -s http://localhost:8000/health >> /tmp/health_check.log 2>&1
EOF

# Install cron (uncomment the line below when ready)
# crontab /tmp/my_cron

# Verify
# crontab -l

# Remove cron
# crontab -r
```

**Cron format:** `minute hour day-of-month month day-of-week command`

### Exercise 1.C.11 — Networking File Transfer with scp and rsync

```bash
# scp: copy a file to/from a remote server (simulated locally)
# scp file.txt user@server:/path/
# scp user@server:/path/file.txt .

# rsync: synchronize directories (better than scp for large transfers)
mkdir -p /tmp/source /tmp/dest
echo "file1" > /tmp/source/a.txt
echo "file2" > /tmp/source/b.txt

rsync -av /tmp/source/ /tmp/dest/

# Modify one file and re-sync (only changed file transfers)
echo "file1 updated" > /tmp/source/a.txt
rsync -av /tmp/source/ /tmp/dest/

# Verify
cat /tmp/dest/a.txt

# Clean up
rm -rf /tmp/source /tmp/dest
```

**Key:** `rsync -av` only transfers changed files. For large deployments, this is much faster than `scp`.

### Exercise 1.C.12 — System Service Management

```bash
# List all running services
systemctl list-units --type=service --state=running 2>/dev/null | head -20

# Check SSH service status (if available)
systemctl status sshd 2>/dev/null || echo "sshd not available (container or minimal system)"

# Check Docker service
systemctl status docker 2>/dev/null || echo "Docker not managed by systemd here"
```

### Exercise 1.C.13 — Inspecting Network Connections from Linux

```bash
# List all listening ports
ss -tulnp

# List all TCP connections
ss -tnp

# Check if a specific port is in use
ss -tulnp | grep 8000

# Alternative: netstat (older tool)
netstat -tulnp 2>/dev/null | head -10
```

### Exercise 1.C.14 — Using sed for Stream Editing

```bash
# Replace text in-place
cp /tmp/linux-lab/logs/app.log /tmp/linux-lab/logs/app_edit.log

# Replace "ERROR" with "CRITICAL"
sed -i 's/ERROR/CRITICAL/g' /tmp/linux-lab/logs/app_edit.log
grep "CRITICAL" /tmp/linux-lab/logs/app_edit.log

# Delete lines matching a pattern
sed -i '/INFO/d' /tmp/linux-lab/logs/app_edit.log
cat /tmp/linux-lab/logs/app_edit.log

# Insert text at line 1
sed -i '1i\# Log file modified by sed' /tmp/linux-lab/logs/app_edit.log
head -3 /tmp/linux-lab/logs/app_edit.log
```

### Exercise 1.C.15 — Process Monitoring with ps and top

```bash
# Show top CPU-consuming processes
ps aux --sort=-%cpu | head -10

# Show top memory-consuming processes
ps aux --sort=-%mem | head -10

# Show a specific user's processes
ps -u $(whoami) -o pid,ppid,%cpu,%mem,cmd --sort=-%cpu

# Real-time monitoring (non-interactive, one snapshot)
top -bn1 | head -30
```

### Exercise 1.C.16 — Writing a Bash Script with Error Handling

```bash
cat > /tmp/linux-lab/scripts/safe_deploy.sh <<'SCRIPT'
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, and pipe failures

APP_DIR="${1:?Usage: $0 <app-directory>}"

echo "=== Deploying from $APP_DIR ==="

# Check directory exists
if [[ ! -d "$APP_DIR" ]]; then
    echo "ERROR: $APP_DIR does not exist" >&2
    exit 1
fi

# Check pyproject.toml exists
if [[ ! -f "$APP_DIR/pyproject.toml" ]]; then
    echo "ERROR: No pyproject.toml found in $APP_DIR" >&2
    exit 1
fi

echo "✓ Directory exists"
echo "✓ pyproject.toml found"
echo "=== Deployment checks passed ==="
SCRIPT
chmod +x /tmp/linux-lab/scripts/safe_deploy.sh

# Test with valid directory
/tmp/linux-lab/scripts/safe_deploy.sh /tmp/linux-lab

# Test with invalid directory
/tmp/linux-lab/scripts/safe_deploy.sh /nonexistent || echo "Script failed as expected"

# Test with no arguments
/tmp/linux-lab/scripts/safe_deploy.sh 2>/dev/null || echo "Script failed with no args as expected"
```

**Key:** `set -euo pipefail` is the #1 most important line in any bash script. Without it, errors are silently ignored.

### Exercise 1.C.17 — Here Documents and Here Strings

```bash
# Here document: multi-line input to a command
cat <<EOF > /tmp/linux-lab/config/app.yaml
server:
  host: 0.0.0.0
  port: 8000
logging:
  level: INFO
  format: json
EOF
cat /tmp/linux-lab/config/app.yaml

# Here string: single-line input
grep "port" <<< "server runs on port 8000"
```

### Exercise 1.C.18 — Using tee for Split Output

```bash
# Write to file AND show on screen
echo "Build started at $(date)" | tee /tmp/linux-lab/logs/build.log

# Append mode
echo "Step 1: Install deps" | tee -a /tmp/linux-lab/logs/build.log
echo "Step 2: Run tests" | tee -a /tmp/linux-lab/logs/build.log

cat /tmp/linux-lab/logs/build.log
```

### Exercise 1.C.19 — Conditional Execution Patterns

```bash
# Run second command only if first succeeds
mkdir -p /tmp/test_dir && echo "Directory created"

# Run second command only if first fails
ls /nonexistent 2>/dev/null || echo "File not found, using default"

# Chain with error handling
cd /tmp/linux-lab && \
    echo "In project dir" && \
    ls pyproject.toml 2>/dev/null || echo "No pyproject.toml here"
```

### Exercise 1.C.20 — Comparing Files

```bash
# Create two similar files
echo -e "line1\nline2\nline3" > /tmp/file_a.txt
echo -e "line1\nline2 modified\nline3\nline4" > /tmp/file_b.txt

# diff: show differences
diff /tmp/file_a.txt /tmp/file_b.txt

# diff unified format (like git diff)
diff -u /tmp/file_a.txt /tmp/file_b.txt

# comm: show common/unique lines (files must be sorted)
sort /tmp/file_a.txt > /tmp/sorted_a.txt
sort /tmp/file_b.txt > /tmp/sorted_b.txt
comm /tmp/sorted_a.txt /tmp/sorted_b.txt

# Clean up
rm /tmp/file_a.txt /tmp/file_b.txt /tmp/sorted_a.txt /tmp/sorted_b.txt
```

---

## PART D — ADVANCED DEBUG LAB (10 Exercises)

### Exercise 1.D.1 — Debug: "Address Already in Use"

**Scenario:** You try to start uvicorn but get `OSError: [Errno 98] Address already in use`.

```bash
# Simulate: start something on port 8000
python3 -c "
import socket, time
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 8000))
s.listen(1)
print(f'Listening on 8000, PID: {__import__(\"os\").getpid()}')
time.sleep(300)
" &

sleep 1

# Now try to start another listener (this will fail)
python3 -c "
import socket
s = socket.socket()
s.bind(('0.0.0.0', 8000))
" 2>&1 || echo "FAILED: Address already in use"

# Diagnose: who is using port 8000?
ss -tulnp | grep 8000

# Fix: kill the offending process
kill $(ss -tulnp | grep 8000 | grep -oP 'pid=\K[0-9]+')

# Verify: port is free
ss -tulnp | grep 8000
```

### Exercise 1.D.2 — Debug: "Permission Denied" on Script Execution

**Scenario:** A deployment script fails with `Permission denied`.

```bash
# Create a script without execute permission
echo '#!/bin/bash' > /tmp/broken_deploy.sh
echo 'echo "Deploying..."' >> /tmp/broken_deploy.sh

# Try to run it
/tmp/broken_deploy.sh 2>&1 || echo "FAILED"

# Diagnose
ls -l /tmp/broken_deploy.sh
file /tmp/broken_deploy.sh

# Fix
chmod +x /tmp/broken_deploy.sh
/tmp/broken_deploy.sh

# Clean up
rm /tmp/broken_deploy.sh
```

### Exercise 1.D.3 — Debug: Orphaned Background Process Eating CPU

**Scenario:** Someone started a process and forgot about it. CPU usage is high.

```bash
# Create a CPU-eating process
python3 -c "
while True:
    pass
" &
CPU_PID=$!

sleep 2

# Diagnose: find high-CPU processes
ps aux --sort=-%cpu | head -5

# Confirm it's the python process
ps -p $CPU_PID -o pid,%cpu,%mem,etime,cmd

# Kill it
kill $CPU_PID

# Verify CPU drops
sleep 1
ps aux --sort=-%cpu | head -5
```

### Exercise 1.D.4 — Debug: Disk Full — Can't Write Logs

**Scenario:** Application crashes because `/tmp` is full (simulated).

```bash
# Check current disk usage
df -h /tmp

# Find the largest files/directories
du -sh /tmp/* 2>/dev/null | sort -rh | head -10

# Find files over 50MB
find /tmp -type f -size +50M 2>/dev/null

# Find old files (not modified in 7 days)
find /tmp -type f -mtime +7 2>/dev/null | head -20

# In production, you would clean old logs:
# find /var/log/app -name "*.log" -mtime +30 -delete
```

### Exercise 1.D.5 — Debug: Shell Script Fails Silently

**Scenario:** A script runs but doesn't do what it should. No errors shown.

```bash
cat > /tmp/silent_fail.sh <<'EOF'
#!/bin/bash
# BUG: No set -euo pipefail

cd /nonexistent_directory
echo "Current directory: $(pwd)"
rm -rf important_data/
echo "Cleanup complete"
EOF
chmod +x /tmp/silent_fail.sh

# Run it — it "succeeds" but didn't actually cd
/tmp/silent_fail.sh

# Now fix it
cat > /tmp/silent_fail_fixed.sh <<'EOF'
#!/bin/bash
set -euo pipefail

cd /nonexistent_directory  # This will now FAIL and stop
echo "Current directory: $(pwd)"
rm -rf important_data/
echo "Cleanup complete"
EOF
chmod +x /tmp/silent_fail_fixed.sh

# Run the fixed version — it fails loudly
/tmp/silent_fail_fixed.sh 2>&1 || echo "Script correctly failed"

# Clean up
rm /tmp/silent_fail.sh /tmp/silent_fail_fixed.sh
```

**Lesson:** Without `set -euo pipefail`, `cd /nonexistent` fails silently and `rm -rf` runs in the *current directory* instead. This has caused real production data loss.

### Exercise 1.D.6 — Debug: Wrong PATH Causes Wrong Python

```bash
# Show which python you're using
which python3
python3 --version

# Simulate wrong PATH priority
mkdir -p /tmp/fake_bin
cat > /tmp/fake_bin/python3 <<'EOF'
#!/bin/bash
echo "WRONG PYTHON! Version 2.7.0"
EOF
chmod +x /tmp/fake_bin/python3

# Prepend fake bin to PATH
export PATH="/tmp/fake_bin:$PATH"
which python3  # Now points to fake
python3  # Shows "WRONG PYTHON!"

# Fix: remove fake from PATH
export PATH=$(echo $PATH | tr ':' '\n' | grep -v fake_bin | tr '\n' ':' | sed 's/:$//')
which python3

# Clean up
rm -rf /tmp/fake_bin
```

### Exercise 1.D.7 — Debug: Deleted File Still Consuming Disk

```bash
# Create a large file and open it
python3 -c "
import time
f = open('/tmp/large_held.dat', 'w')
for i in range(1000000):
    f.write('x' * 100 + '\n')
f.flush()
print(f'File written. PID: {__import__(\"os\").getpid()}')
time.sleep(300)
" &

HELD_PID=$!
sleep 2

# Check file size
ls -lh /tmp/large_held.dat

# Delete the file
rm /tmp/large_held.dat

# File is "gone" from ls
ls /tmp/large_held.dat 2>&1 || echo "File not found (but space still used!)"

# Prove the space is still held
ls -la /proc/$HELD_PID/fd/ | grep deleted

# Fix: kill the process to release the space
kill $HELD_PID

# Now the space is truly freed
```

**Production scenario:** Log rotation deletes old log files, but the application still holds them open. Disk stays full until the app is restarted.

### Exercise 1.D.8 — Debug: Environment Variable Inheritance

```bash
# Set a variable WITHOUT export
SECRET_KEY="abc123"

# Try to use it in a child process
bash -c 'echo "SECRET_KEY=$SECRET_KEY"'  # Empty!

# Fix: export it
export SECRET_KEY="abc123"
bash -c 'echo "SECRET_KEY=$SECRET_KEY"'  # Now it works

# Lesson: non-exported variables are invisible to child processes
unset SECRET_KEY
```

### Exercise 1.D.9 — Debug: Script Works in Terminal but Fails in Cron

**Scenario:** A cron job fails because cron has a minimal environment.

```bash
# Show what environment cron sees (minimal)
env -i /bin/bash -c 'echo PATH=$PATH'
# Output: PATH= (empty!)

# Your script relies on $PATH to find commands
env -i /bin/bash -c 'which python3' 2>&1 || echo "FAIL: python3 not found in cron environment"

# Fix: use absolute paths in cron scripts
cat > /tmp/cron_safe.sh <<'EOF'
#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin"
/usr/bin/python3 -c "print('Cron job ran successfully')"
EOF
chmod +x /tmp/cron_safe.sh
env -i /bin/bash /tmp/cron_safe.sh

rm /tmp/cron_safe.sh
```

### Exercise 1.D.10 — Debug: SSH Connection Drops Kill Your Server

**Scenario:** You start uvicorn over SSH. You lose network connectivity. The server dies.

```bash
# Simulate: start a process attached to terminal
echo "Starting server..."
sleep 120 &
SERVER_PID=$!

# Sending SIGHUP (what happens when terminal closes)
kill -HUP $SERVER_PID
wait $SERVER_PID 2>/dev/null
ps -p $SERVER_PID 2>/dev/null || echo "Process died on SIGHUP"

# Fix 1: nohup
nohup sleep 120 &
NOHUP_PID=$!
kill -HUP $NOHUP_PID
sleep 1
ps -p $NOHUP_PID && echo "Process survived SIGHUP with nohup"
kill $NOHUP_PID

# Fix 2 (better): Use tmux (shown in Exercise 1.C.9)
# Fix 3 (best): Use systemd service file for production
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Server Health Check System

**Situation:** You're the on-call engineer. You receive an alert: "Service on production server is unresponsive."

**Your task:** Write a comprehensive health-check script that:
1. Checks if the process is running
2. Checks if the port is listening
3. Checks disk space
4. Checks memory
5. Checks recent error logs
6. Reports all findings

```bash
cat > /tmp/linux-lab/scripts/healthcheck.sh <<'SCRIPT'
#!/bin/bash
set -euo pipefail

SERVICE_PORT=${1:-8000}
LOG_DIR=${2:-/tmp/linux-lab/logs}
ERRORS=0

echo "=============================="
echo "  HEALTH CHECK REPORT"
echo "  $(date)"
echo "=============================="

# 1. Check if anything is listening on the port
echo -n "[PORT $SERVICE_PORT] "
if ss -tulnp | grep -q ":$SERVICE_PORT "; then
    echo "✓ LISTENING"
else
    echo "✗ NOT LISTENING"
    ERRORS=$((ERRORS + 1))
fi

# 2. Check disk space (alert if >80%)
echo -n "[DISK] "
DISK_USAGE=$(df / --output=pcent | tail -1 | tr -d ' %')
if [[ $DISK_USAGE -lt 80 ]]; then
    echo "✓ ${DISK_USAGE}% used"
else
    echo "✗ ${DISK_USAGE}% used (CRITICAL)"
    ERRORS=$((ERRORS + 1))
fi

# 3. Check available memory
echo -n "[MEMORY] "
AVAIL_MB=$(free -m | awk '/Mem:/ {print $7}')
if [[ $AVAIL_MB -gt 500 ]]; then
    echo "✓ ${AVAIL_MB}MB available"
else
    echo "✗ ${AVAIL_MB}MB available (LOW)"
    ERRORS=$((ERRORS + 1))
fi

# 4. Check for recent errors in logs
echo -n "[LOGS] "
if [[ -d "$LOG_DIR" ]]; then
    ERROR_COUNT=$(grep -c "ERROR\|CRITICAL" "$LOG_DIR"/*.log 2>/dev/null || echo 0)
    if [[ "$ERROR_COUNT" == "0" ]]; then
        echo "✓ No errors in logs"
    else
        echo "⚠ ${ERROR_COUNT} error(s) found"
    fi
else
    echo "⚠ Log directory not found"
fi

# 5. Check CPU load
echo -n "[CPU] "
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk -F, '{print $1}' | tr -d ' ')
echo "Load average: $LOAD"

echo "=============================="
if [[ $ERRORS -gt 0 ]]; then
    echo "RESULT: ✗ UNHEALTHY ($ERRORS issues found)"
    exit 1
else
    echo "RESULT: ✓ HEALTHY"
    exit 0
fi
SCRIPT
chmod +x /tmp/linux-lab/scripts/healthcheck.sh
```

**Test it:**
```bash
/tmp/linux-lab/scripts/healthcheck.sh 8000 /tmp/linux-lab/logs
```

**Acceptance Criteria:**
- [ ] Script runs without errors
- [ ] Reports port status correctly
- [ ] Reports disk usage
- [ ] Reports memory availability
- [ ] Checks logs for errors
- [ ] Exits with code 1 if any check fails
- [ ] Can be added to cron for periodic monitoring

**Validation:**
```bash
# Make it fail by checking a port that's not listening
/tmp/linux-lab/scripts/healthcheck.sh 9999 /tmp/linux-lab/logs
echo "Exit code: $?"  # Should be 1
```

---

## Key Takeaways

1. **Every command is a process.** Understanding fork→exec→wait is the foundation of everything else.
2. **Permissions exist for a reason.** If something won't run, check `ls -l` before Stack Overflow.
3. **`set -euo pipefail`** in every bash script. No exceptions.
4. **Background processes need supervision.** Use tmux, nohup, or systemd — never bare `&` in production.
5. **Logs are your best friend.** Learn grep, awk, tail -f, and they'll serve you for decades.
6. **File descriptors are invisible leaks.** Deleted files held by a process still consume disk.

---

*Next: [Section 2 — Git & Version Control](02-git-version-control.md)*
