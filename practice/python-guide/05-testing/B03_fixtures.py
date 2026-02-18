"""
Exercise 5.B.3 — Fixtures for Test Data
Guide: docs/python-guide/05-testing-with-pytest.md
"""
import pytest


@pytest.fixture
def sample_user():
    """Fixture that provides a sample user dictionary."""
    # TODO: return {"name": "Alice", "email": "alice@test.com", "age": 30}
    pass


@pytest.fixture
def product_list():
    """Fixture that provides a list of products."""
    # TODO: return [{"name": "Widget", "price": 9.99}, ...]
    pass


@pytest.fixture
def temp_file(tmp_path):
    """Fixture that creates a temporary file with test content."""
    # TODO: f = tmp_path / "test.txt"
    # f.write_text("test content")
    # return f
    pass


@pytest.fixture
def configured_logger():
    """Fixture that provides a configured logger."""
    # TODO: import logging
    # return logging.getLogger("test")
    pass


def test_user_has_name(sample_user):
    # TODO: assert sample_user["name"] == "Alice"
    pass


def test_products_not_empty(product_list):
    # TODO: assert len(product_list) > 0
    pass


def test_temp_file_exists(temp_file):
    # TODO: assert temp_file.exists()
    pass
