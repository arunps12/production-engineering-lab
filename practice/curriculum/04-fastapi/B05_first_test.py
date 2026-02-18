"""
Exercise 4.B.5 — Write Your First Test
Guide: docs/curriculum/04-fastapi-professional.md

Run: pytest practice/curriculum/04-fastapi/B05_first_test.py -v
"""

# TODO: pip install httpx pytest
# from fastapi.testclient import TestClient
# from B01_B02_app import app  # Import your app

# client = TestClient(app)


def test_health():
    """Test health endpoint returns 200."""
    # TODO: response = client.get("/health")
    # assert response.status_code == 200
    # assert response.json()["status"] == "healthy"
    pass


def test_version():
    """Test version endpoint returns version string."""
    # TODO: response = client.get("/version")
    # assert response.status_code == 200
    # assert "version" in response.json()
    pass


def test_predict():
    """Test prediction endpoint."""
    # TODO: response = client.post("/predict", json={...})
    # assert response.status_code == 200
    # assert "prediction" in response.json()
    pass


def test_predict_invalid():
    """Test prediction endpoint with invalid data returns 422."""
    # TODO: response = client.post("/predict", json={"bad": "data"})
    # assert response.status_code == 422
    pass
