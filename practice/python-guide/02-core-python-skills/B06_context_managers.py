"""
Exercise 2.B.6 — Context Managers (with statement)
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Use 'with' for file operations
2. Create a custom context manager using __enter__/__exit__
3. Create a context manager using @contextmanager decorator
4. Understand why context managers are important (resource cleanup)
"""

from contextlib import contextmanager


# TODO: File operations with 'with'


# TODO: Custom context manager class
class Timer:
    """Context manager that measures execution time."""

    def __enter__(self):
        # TODO: Record start time
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: Calculate and print elapsed time
        pass


# TODO: Context manager using decorator
@contextmanager
def temporary_directory():
    """Create a temp directory, yield it, then clean up."""
    # TODO: Implement
    pass


# TODO: Test your context managers
