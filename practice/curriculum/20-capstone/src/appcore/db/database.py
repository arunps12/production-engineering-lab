# =============================================================================
# Section 04 — Database Connection Manager
# Guide: docs/curriculum/20-capstone-project.md
#
# Exercise: Implement SQLite database with context manager.
#
# TODO:
# 1. Create DATABASE_PATH constant (use pathlib)
# 2. Implement get_db() context manager that:
#    - Opens a sqlite3 connection
#    - Sets row_factory = sqlite3.Row
#    - Yields the connection
#    - Commits on success, rolls back on exception
#    - Always closes the connection
# 3. Implement init_db() that creates the predictions table:
#    - id INTEGER PRIMARY KEY AUTOINCREMENT
#    - input_text TEXT NOT NULL
#    - result TEXT NOT NULL
#    - confidence REAL NOT NULL
#    - created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# =============================================================================

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DATABASE_PATH = Path("data/predictions.db")


@contextmanager
def get_db():
    """Yield a SQLite connection with automatic commit/rollback."""
    # TODO: Implement context manager
    pass


def init_db():
    """Create tables if they don't exist."""
    # TODO: Create predictions table
    pass
