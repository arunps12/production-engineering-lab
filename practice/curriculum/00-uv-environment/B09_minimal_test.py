"""
Exercise 0.B.9 — Write and Run a Minimal Test
Guide: docs/curriculum/00-uv-python-environment.md
"""


def test_python_version():
    """Verify Python version is 3.11+."""
    import sys
    assert sys.version_info >= (3, 11), f"Need Python 3.11+, got {sys.version}"


def test_imports():
    """Verify key packages are importable."""
    # TODO: Add import checks for your project dependencies
    # import fastapi
    # import uvicorn
    pass


# Run: uv run pytest practice/curriculum/00-uv-environment/B09_minimal_test.py -v
