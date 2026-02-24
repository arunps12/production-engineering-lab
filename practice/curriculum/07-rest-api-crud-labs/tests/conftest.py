"""Pytest fixtures for CRUD API tests."""

import pytest
from fastapi.testclient import TestClient

from src.crud_api.main import app
from src.crud_api.database import db


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test."""
    db.reset()
    yield


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)
