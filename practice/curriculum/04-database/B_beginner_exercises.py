"""
Section 4 — Database: Beginner Exercises (B1-B7)
Guide: docs/curriculum/04-database-fundamentals.md
"""
import sqlite3


# Exercise 9.B.1 — SQLite Basics
def create_database():
    """Create a users table and insert sample data."""
    # TODO: conn = sqlite3.connect("practice.db")
    # TODO: CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)
    # TODO: INSERT sample data
    # TODO: SELECT and print all users
    pass


# Exercise 9.B.2 — CRUD Operations
def create_task(title: str):
    """Create a new task."""
    # TODO: INSERT INTO tasks (title, completed, created_at) VALUES (?, 0, datetime('now'))
    pass


def get_tasks(completed: bool = None):
    """Get tasks, optionally filtered by completion status."""
    # TODO: SELECT * FROM tasks
    pass


def update_task(task_id: int, completed: bool):
    """Mark a task as completed or not."""
    # TODO: UPDATE tasks SET completed = ? WHERE id = ?
    pass


def delete_task(task_id: int):
    """Delete a task."""
    # TODO: DELETE FROM tasks WHERE id = ?
    pass


# Exercise 9.B.3 — SQL Queries Practice
def query_exercises():
    """Practice SQL queries."""
    # TODO: 1. Select all incomplete tasks
    # TODO: 2. Count tasks per completion status
    # TODO: 3. Find the most recently created task
    # TODO: 4. Update old tasks to completed
    # TODO: 5. Delete old completed tasks
    pass


# Exercise 9.B.7 — Database Connection Context Manager
class DatabaseConnection:
    """Context manager for database connections."""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self):
        # TODO: Open connection
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: Commit or rollback, then close
        pass


if __name__ == "__main__":
    create_database()
