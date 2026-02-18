#!/usr/bin/env python3
"""
Exercise 7.B.4 — CLI Tool with argparse
Guide: docs/python-guide/07-system-automation-scripting.md
"""
import argparse
from pathlib import Path


def find_files(directory: str, pattern: str, min_size: int = 0, show_size: bool = False):
    """Find files matching a pattern in a directory.

    Args:
        directory: Root directory to search
        pattern: Glob pattern (e.g., '*.py', '*.log')
        min_size: Minimum file size in bytes (0 = no minimum)
        show_size: Whether to show file sizes
    """
    # TODO: Implement file search
    # root = Path(directory)
    # if not root.is_dir():
    #     print(f"Error: {directory} is not a directory")
    #     return
    #
    # count = 0
    # for path in sorted(root.rglob(pattern)):
    #     if path.is_file() and path.stat().st_size >= min_size:
    #         if show_size:
    #             size = path.stat().st_size
    #             print(f"{path}  ({size} bytes)")
    #         else:
    #             print(path)
    #         count += 1
    # print(f"\nFound {count} file(s)")
    pass


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        description="Find files matching a pattern",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s . '*.py'                     Find Python files
  %(prog)s /var/log '*.log' --min-size 1024  Find logs > 1KB
  %(prog)s . '*.txt' --show-size        Show file sizes
""",
    )

    # TODO: Add arguments:
    # parser.add_argument("directory", help="Directory to search")
    # parser.add_argument("pattern", help="Glob pattern to match")
    # parser.add_argument("--min-size", type=int, default=0, help="Min file size (bytes)")
    # parser.add_argument("--show-size", action="store_true", help="Show file sizes")

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    # TODO: find_files(args.directory, args.pattern, args.min_size, args.show_size)
