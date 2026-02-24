# =============================================================================
# Section 04 — Database Tests
# Guide: docs/curriculum/20-capstone-project.md
#
# Exercise: Write tests for the database layer.
#
# TODO:
# 1. Test init_db creates the predictions table
# 2. Test save_prediction returns an ID
# 3. Test get_prediction retrieves saved data
# 4. Test list_predictions returns correct order and limit
# 5. Test get_prediction returns None for missing ID
# =============================================================================

# import pytest
# from appcore.db.database import init_db, get_db
# from appcore.db.repository import save_prediction, get_prediction, list_predictions


# @pytest.fixture(autouse=True)
# def setup_db(tmp_path, monkeypatch):
#     """Use a temporary database for each test."""
#     # TODO: Monkeypatch DATABASE_PATH to tmp_path / "test.db"
#     # TODO: Call init_db()
#     pass


# def test_save_and_get_prediction():
#     """Save a prediction and retrieve it."""
#     # TODO: Implement
#     pass


# def test_list_predictions_order():
#     """Predictions should be returned newest first."""
#     # TODO: Implement
#     pass


# def test_get_missing_prediction():
#     """Getting a non-existent prediction should return None."""
#     # TODO: Implement
#     pass
