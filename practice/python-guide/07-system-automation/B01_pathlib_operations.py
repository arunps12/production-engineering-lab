"""
Exercise 7.B.1 — pathlib File Operations
Guide: docs/python-guide/07-system-automation-scripting.md
"""
from pathlib import Path


def explore_pathlib():
    """Practice pathlib operations."""
    # TODO 1: Create a Path object for the current working directory
    # current = Path.cwd()
    # print(f"CWD: {current}")

    # TODO 2: Create a directory structure: tmp_practice/logs/archive
    # base = Path("tmp_practice")
    # (base / "logs" / "archive").mkdir(parents=True, exist_ok=True)

    # TODO 3: Create 5 sample log files
    # for i in range(5):
    #     (base / "logs" / f"app_{i}.log").write_text(f"Log entry {i}\n")

    # TODO 4: List all .log files using glob
    # for log in (base / "logs").glob("*.log"):
    #     print(f"Found: {log.name}, Size: {log.stat().st_size} bytes")

    # TODO 5: Rename app_0.log -> app_0.log.bak
    # old = base / "logs" / "app_0.log"
    # old.rename(old.with_suffix(".log.bak"))

    # TODO 6: Read and print contents of all remaining .log files
    # for log in sorted((base / "logs").glob("*.log")):
    #     print(f"{log.name}: {log.read_text().strip()}")
    pass


if __name__ == "__main__":
    explore_pathlib()
