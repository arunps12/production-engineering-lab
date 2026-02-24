# =============================================================================
# Section 04 — Prediction Repository (CRUD)
# Guide: docs/curriculum/20-capstone-project.md
#
# Exercise: Implement repository pattern for prediction storage.
#
# TODO:
# 1. Implement save_prediction(input_text, result, confidence) -> int
#    - Insert into predictions table
#    - Return the new row ID
# 2. Implement get_prediction(prediction_id) -> dict | None
#    - Fetch single prediction by ID
#    - Return dict or None if not found
# 3. Implement list_predictions(limit=50) -> list[dict]
#    - Return recent predictions ordered by created_at DESC
# =============================================================================

from appcore.db.database import get_db


def save_prediction(input_text: str, result: str, confidence: float) -> int:
    """Save a prediction and return its ID."""
    # TODO: INSERT into predictions table
    pass


def get_prediction(prediction_id: int) -> dict | None:
    """Fetch a single prediction by ID."""
    # TODO: SELECT by ID
    pass


def list_predictions(limit: int = 50) -> list[dict]:
    """List recent predictions."""
    # TODO: SELECT with ORDER BY and LIMIT
    pass
