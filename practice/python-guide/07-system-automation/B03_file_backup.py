"""
Exercise 7.B.3 — File Backup Script
Guide: docs/python-guide/07-system-automation-scripting.md
"""
import shutil
from pathlib import Path
from datetime import datetime


def backup_directory(source: str, backup_root: str = "backups") -> Path:
    """Create a timestamped backup of a directory.

    Args:
        source: Directory to back up
        backup_root: Where to store backups

    Returns:
        Path to the created backup
    """
    # TODO 1: Validate source exists and is a directory
    # src = Path(source)
    # if not src.is_dir():
    #     raise ValueError(f"Source is not a directory: {source}")

    # TODO 2: Create backup directory with timestamp
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # backup_dir = Path(backup_root)
    # backup_dir.mkdir(parents=True, exist_ok=True)

    # TODO 3: Create archive (.tar.gz) of source directory
    # archive_name = f"{src.name}_{timestamp}"
    # archive_path = shutil.make_archive(
    #     str(backup_dir / archive_name), "gztar", str(src.parent), src.name
    # )

    # TODO 4: Print summary (archive path, size)
    # archive = Path(archive_path)
    # size_mb = archive.stat().st_size / (1024 * 1024)
    # print(f"Backup created: {archive}")
    # print(f"Size: {size_mb:.2f} MB")
    # return archive
    pass


def rotate_backups(backup_root: str = "backups", keep: int = 5):
    """Keep only the N most recent backups, delete older ones.

    Args:
        backup_root: Directory containing backups
        keep: Number of backups to retain
    """
    # TODO: List .tar.gz files sorted by modification time
    # Delete oldest files until only 'keep' remain
    pass


if __name__ == "__main__":
    # Create a test directory structure
    test_src = Path("tmp_backup_test")
    test_src.mkdir(exist_ok=True)
    (test_src / "file1.txt").write_text("hello")
    (test_src / "file2.txt").write_text("world")

    backup_directory(str(test_src))
    rotate_backups(keep=3)
