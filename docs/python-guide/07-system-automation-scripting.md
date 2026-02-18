# SECTION 7 — SYSTEM AUTOMATION & SCRIPTING

---

## PART A — CONCEPT EXPLANATION

### Why Python for Automation?

Python is the go-to language for system automation because:
- **Readable** — Scripts are self-documenting
- **Cross-platform** — Works on Linux, macOS, Windows
- **Battery-included** — `os`, `pathlib`, `subprocess`, `shutil` built in
- **Rich ecosystem** — Fabric, Paramiko, Click for advanced automation
- **Better than bash** — For anything beyond simple commands, Python is more maintainable

### Key Standard Library Modules

```
pathlib    → File paths (modern, preferred over os.path)
subprocess → Run shell commands
shutil     → High-level file operations (copy, move, archive)
os         → Environment variables, process info
argparse   → CLI argument parsing
logging    → Structured logging
tempfile   → Temporary files/directories
glob       → File pattern matching
json/yaml  → Configuration file parsing
```

### pathlib — Modern Path Handling

```python
from pathlib import Path

# Create paths
home = Path.home()
project = Path("/app/my-project")
config = project / "config" / "settings.yaml"  # Path concatenation with /

# Query paths
config.exists()          # True/False
config.is_file()         # True/False
config.is_dir()          # True/False
config.name              # "settings.yaml"
config.stem              # "settings"
config.suffix            # ".yaml"
config.parent            # Path("/app/my-project/config")

# Read/write
content = config.read_text()
config.write_text("key: value")

# List directory
for f in project.iterdir():
    print(f.name)

# Glob pattern matching
for py in project.glob("**/*.py"):
    print(py)
```

### subprocess — Running Commands

```python
import subprocess

# Simple command
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)  # 0 = success

# With error handling
result = subprocess.run(
    ["git", "status"],
    capture_output=True, text=True, check=True  # Raises on non-zero exit
)

# Pipe commands
ps = subprocess.run(["ps", "aux"], capture_output=True, text=True)
grep = subprocess.run(
    ["grep", "python"], input=ps.stdout, capture_output=True, text=True
)
print(grep.stdout)
```

**Security rule**: NEVER use `shell=True` with user input — it enables shell injection.

### argparse — CLI Tool Building

```python
import argparse

parser = argparse.ArgumentParser(description="Deploy tool")
parser.add_argument("environment", choices=["dev", "staging", "prod"])
parser.add_argument("--version", required=True, help="Version to deploy")
parser.add_argument("--dry-run", action="store_true", help="Preview only")
parser.add_argument("-v", "--verbose", action="count", default=0)

args = parser.parse_args()
print(f"Deploying {args.version} to {args.environment}")
```

```bash
python deploy.py prod --version 1.2.0 --dry-run -vv
```

### shutil — File Operations

```python
import shutil

shutil.copy("src.txt", "dst.txt")            # Copy file
shutil.copy2("src.txt", "dst.txt")           # Copy file + metadata
shutil.copytree("src_dir", "dst_dir")        # Copy directory
shutil.move("old_path", "new_path")          # Move/rename
shutil.rmtree("directory")                    # Delete directory
shutil.make_archive("backup", "gztar", "src_dir")  # Create .tar.gz
shutil.disk_usage("/")                        # Disk space info
```

### Common Automation Patterns

**1. File watcher:**
```python
import time
from pathlib import Path

def watch(path, interval=1):
    last_modified = {}
    while True:
        for f in Path(path).glob("**/*"):
            mtime = f.stat().st_mtime
            if f not in last_modified or last_modified[f] != mtime:
                print(f"Changed: {f}")
                last_modified[f] = mtime
        time.sleep(interval)
```

**2. Log rotator:**
```python
def rotate_logs(log_dir, max_size_mb=100):
    for log in Path(log_dir).glob("*.log"):
        size_mb = log.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            archive = log.with_suffix(f".{datetime.now():%Y%m%d}.log.gz")
            compress_and_move(log, archive)
```

**3. Deployment script:**
```python
def deploy(version, environment):
    run_command(f"git checkout v{version}")
    run_command("docker build -t app:latest .")
    run_command(f"docker tag app:latest registry/app:{version}")
    run_command(f"docker push registry/app:{version}")
    run_command(f"kubectl set image deployment/app app=registry/app:{version}")
```

### Common Beginner Misunderstandings

1. **"Use os.path for paths"** — `pathlib` is the modern replacement. It's cleaner, object-oriented, and cross-platform.
2. **"subprocess.run with shell=True is easier"** — It's a security vulnerability. Always pass commands as lists.
3. **"Bash is better for automation"** — For simple commands, yes. For logic, error handling, testing — Python wins.
4. **"argparse is too complex"** — For production tools, proper argument parsing prevents user errors. `click` is a good alternative.
5. **"Just use os.system()"** — `os.system()` is deprecated for subprocess use. Use `subprocess.run()` instead.

---

## PART B — BEGINNER PRACTICE

### Exercise 7.B.1 — Path Operations

Use `pathlib` to:
1. List all `.py` files in a directory recursively
2. Find the largest file in a directory
3. Count files by extension
4. Create a directory tree: `project/src/utils/`

### Exercise 7.B.2 — Run Shell Commands

Use `subprocess.run` to:
1. Get the current git branch
2. List running Docker containers
3. Check disk usage
4. Ping a host and check success

### Exercise 7.B.3 — File Backup Script

Write a script that:
1. Takes a source directory as argument
2. Creates a timestamped `.tar.gz` backup
3. Stores it in a `backups/` directory
4. Deletes backups older than 7 days

### Exercise 7.B.4 — CLI Tool with argparse

Build a `sysinfo` CLI tool:
```bash
python sysinfo.py --cpu          # Show CPU info
python sysinfo.py --memory       # Show memory info
python sysinfo.py --disk         # Show disk usage
python sysinfo.py --all          # Show everything
python sysinfo.py --json         # Output as JSON
```

### Exercise 7.B.5 — Environment Setup Script

Write a script that:
1. Checks if Python 3.11+ is installed
2. Creates a virtual environment
3. Installs dependencies from `requirements.txt`
4. Runs tests to verify setup
5. Prints a success/failure summary

### Exercise 7.B.6 — Log File Analyzer

Write a script that parses a log file:
```
2025-01-01 10:00:00 INFO Request received
2025-01-01 10:00:01 ERROR Database connection failed
2025-01-01 10:00:02 WARNING High memory usage
```

Output:
- Count per log level (INFO: 50, ERROR: 3, WARNING: 10)
- All ERROR lines
- Time range of the log

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 7.C.1 — Deployment Automation Script

Build a deploy script with:
- Pre-deployment checks (tests pass, branch is main)
- Docker build with version tag
- Health check after deployment
- Rollback on failure
- Dry-run mode

### Exercise 7.C.2 — System Health Monitor

Write a monitoring script that checks:
- CPU usage (warn if > 80%)
- Memory usage (warn if > 80%)
- Disk usage (warn if > 90%)
- Service availability (HTTP health check)
- Output as JSON for machine consumption

### Exercise 7.C.3 — Configuration Management

Build a config tool that:
- Reads config from YAML/JSON files
- Supports environment overrides (`CONFIG_DB_HOST` → `db.host`)
- Validates required fields
- Generates example config files

### Exercise 7.C.4 — Cron Job Script

Write a Python cron job that:
- Runs database backups every night
- Cleans up old log files weekly
- Reports system health hourly
- Handles errors and sends notifications

### Exercise 7.C.5 — SSH Automation

Use `subprocess` (or `paramiko`) to automate remote server tasks:
```python
def ssh_command(host, command):
    result = subprocess.run(
        ["ssh", f"user@{host}", command],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout, result.returncode
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 7.D.1 — Debug: subprocess Hangs

Symptom: `subprocess.run()` never returns.
Cause: Process produces too much output, filling the pipe buffer.
Task: Fix with `capture_output=True` or stream output incrementally.

### Exercise 7.D.2 — Debug: Path Encoding Issues

Symptom: Script crashes on filenames with spaces or unicode characters.
Task: Fix by using `pathlib.Path` objects (not string concatenation) and proper encoding.

### Exercise 7.D.3 — Debug: Permission Denied

Symptom: Script works for you but fails in CI/production.
Task: Check file permissions, user context, script execution bits (`chmod +x`).

### Exercise 7.D.4 — Debug: argparse Errors Aren't Helpful

Symptom: Users get cryptic error messages from argparse.
Task: Add custom error messages, help text, and usage examples.

---

## PART E — PRODUCTION SIMULATION

### Scenario: DevOps Toolkit

Build a comprehensive CLI toolkit (`devtool`) that combines all automation skills:

```bash
devtool deploy prod --version 1.2.0 --dry-run
devtool backup /data --retain 7
devtool health --hosts app1,app2,app3 --format json
devtool logs /var/log/app --level ERROR --since "1 hour ago"
devtool cleanup --logs --backups --older-than 30d
```

Requirements:
1. Proper CLI with subcommands (use argparse or click)
2. Logging at appropriate levels
3. Error handling and exit codes
4. JSON output option for machine consumption
5. Dry-run mode for destructive operations
6. Configuration file support
7. Tests for each subcommand

---

## Key Takeaways

1. **pathlib over os.path** — Always use `pathlib.Path` for file operations.
2. **subprocess.run over os.system** — Never use shell=True with untrusted input.
3. **argparse for CLI tools** — Proper argument parsing prevents user errors.
4. **Automate everything you do twice** — If you'll do it again, script it.
5. **Error handling is critical** — Scripts run unattended. They must handle failures gracefully.
6. **Test your scripts** — Automation scripts are code. They deserve tests too.

---
*Previous: [Section 6 — Concurrency & Async Python](06-concurrency-async.md)*
