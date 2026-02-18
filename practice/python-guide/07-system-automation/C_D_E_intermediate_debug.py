"""
Section 7 — System Automation: Intermediate (C1-C5) + Debug (D1-D4) + Production (E1)
Guide: docs/python-guide/07-system-automation-scripting.md
"""
import subprocess
from pathlib import Path
import argparse
import json
import shutil
import time


# ──────────────────────────────────────────────
# Exercise 7.C.1 — Log File Analyzer
# ──────────────────────────────────────────────
def analyze_logs(log_dir: str, pattern: str = "ERROR"):
    """Analyze log files for a specific pattern.

    Args:
        log_dir: Directory containing log files
        pattern: Pattern to search for (default: ERROR)
    """
    # TODO: Walk log_dir, read each .log file, count lines matching pattern
    # Print per-file and total counts
    # Use pathlib for paths, open() for reading
    pass


# ──────────────────────────────────────────────
# Exercise 7.C.2 — Environment Setup Script
# ──────────────────────────────────────────────
def setup_environment(project_dir: str):
    """Create a development environment for a project.

    Steps:
    1. Create virtual environment
    2. Install requirements.txt if it exists
    3. Create .env from .env.example if it exists
    4. Run any setup scripts
    """
    # TODO: project = Path(project_dir)
    # subprocess.run(["python3", "-m", "venv", str(project / ".venv")], check=True)
    # venv_pip = project / ".venv" / "bin" / "pip"
    # if (project / "requirements.txt").exists():
    #     subprocess.run([str(venv_pip), "install", "-r", "requirements.txt"], cwd=str(project))
    # ...
    pass


# ──────────────────────────────────────────────
# Exercise 7.C.3 — System Health Monitor
# ──────────────────────────────────────────────
def check_system_health() -> dict:
    """Check system health and return a report.

    Returns:
        Dict with disk, memory, cpu, and process info
    """
    report = {}
    # TODO: Use subprocess to run system commands:
    # - df -h (disk usage)
    # - free -m (memory) or /proc/meminfo
    # - uptime (load average)
    # - ps aux --sort=-%mem | head -5 (top memory processes)
    # Parse output and build report dict
    return report


# ──────────────────────────────────────────────
# Exercise 7.C.4 — Config File Manager
# ──────────────────────────────────────────────
class ConfigManager:
    """Manage JSON configuration files with env overrides."""

    def __init__(self, config_path: str):
        self.path = Path(config_path)
        self.config: dict = {}
        # TODO: Load config from file if it exists
        # Otherwise create with defaults

    def get(self, key: str, default=None):
        """Get a config value, checking env vars first."""
        # TODO: import os
        # Check os.environ first (prefix CONFIG_)
        # Then check self.config
        # Then return default
        pass

    def set(self, key: str, value):
        """Set a config value and save."""
        # TODO: self.config[key] = value
        # self.save()
        pass

    def save(self):
        """Save config to JSON file."""
        # TODO: self.path.write_text(json.dumps(self.config, indent=2))
        pass


# ──────────────────────────────────────────────
# Exercise 7.C.5 — Deployment Automation
# ──────────────────────────────────────────────
def deploy(app_dir: str, target: str = "staging"):
    """Simulate a deployment process.

    Steps: test → build → backup → deploy → verify → rollback on failure
    """
    # TODO: Implement each step:
    # 1. Run tests: subprocess.run(["pytest"], cwd=app_dir, check=True)
    # 2. Build: subprocess.run(["python", "setup.py", "build"], ...)
    # 3. Backup current: shutil.copytree(...)
    # 4. Deploy: shutil.copytree(build_dir, deploy_dir)
    # 5. Verify: health check
    # 6. On failure: rollback from backup
    pass


# ──────────────────────────────────────────────
# DEBUG LAB
# ──────────────────────────────────────────────

# Exercise 7.D.1 — subprocess Hangs Forever
def run_command_buggy():
    """BUG: This command hangs because stdout buffer fills up."""
    proc = subprocess.Popen(
        ["find", "/", "-name", "*.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # BUG: proc.wait() will deadlock if output exceeds buffer!
    proc.wait()
    output = proc.stdout.read()
    # TODO: Fix — use proc.communicate(timeout=30) instead
    return output


# Exercise 7.D.2 — Path Encoding Issues
def read_files_buggy(directory: str):
    """BUG: Crashes on filenames with special characters."""
    for f in Path(directory).iterdir():
        print(f.name)
        # BUG: .read_text() crashes if file has non-UTF-8 content
        content = f.read_text()
        print(f"  {len(content)} chars")
    # TODO: Fix — use .read_text(encoding='utf-8', errors='replace')
    # Or use .read_bytes() and handle encoding


# Exercise 7.D.3 — Permissions Error Handling
def copy_files_buggy(src: str, dst: str):
    """BUG: No permission error handling."""
    shutil.copytree(src, dst)
    # TODO: Fix —
    # try:
    #     shutil.copytree(src, dst)
    # except PermissionError as e:
    #     print(f"Permission denied: {e}")
    # except FileExistsError:
    #     print(f"Destination exists: {dst}")


# Exercise 7.D.4 — argparse Silent Failures
def create_parser_buggy():
    """BUG: Missing required arguments cause cryptic errors."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int)  # No default — returns None
    args = parser.parse_args([])
    # BUG: This will crash: int(None)
    print(f"Listening on port {args.port + 1000}")
    # TODO: Fix — add default=8080, or use required=True


# ──────────────────────────────────────────────
# PRODUCTION (E1) — DevOps Toolkit CLI
# ──────────────────────────────────────────────
def build_toolkit_parser() -> argparse.ArgumentParser:
    """Build a multi-command CLI toolkit.

    Commands:
      health    — Run system health check
      backup    — Back up a directory
      deploy    — Deploy an application
      config    — Manage configuration
    """
    parser = argparse.ArgumentParser(description="DevOps Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command")

    # TODO: health subcommand
    # health_parser = subparsers.add_parser("health", help="System health check")
    # health_parser.add_argument("--json", action="store_true")

    # TODO: backup subcommand
    # backup_parser = subparsers.add_parser("backup", help="Backup directory")
    # backup_parser.add_argument("source")
    # backup_parser.add_argument("--keep", type=int, default=5)

    # TODO: deploy subcommand
    # deploy_parser = subparsers.add_parser("deploy", help="Deploy app")
    # deploy_parser.add_argument("app_dir")
    # deploy_parser.add_argument("--target", choices=["staging", "production"], default="staging")

    return parser


if __name__ == "__main__":
    parser = build_toolkit_parser()
    args = parser.parse_args()
    # TODO: Route to appropriate function based on args.command
