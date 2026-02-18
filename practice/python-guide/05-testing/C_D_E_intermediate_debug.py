"""
Section 5 — Testing: Intermediate (C1-C6) + Debug (D1-D4) + Production (E1)
Guide: docs/python-guide/05-testing-with-pytest.md
"""
import pytest


# Exercise 5.C.1 — Mocking External Services
def fetch_user_from_api(user_id: int) -> dict:
    """Fetch user from external API (mock this in tests)."""
    # import requests
    # response = requests.get(f"https://api.example.com/users/{user_id}")
    # return response.json()
    pass


def test_fetch_user_mocked():
    """Test fetch_user without making real HTTP calls."""
    # TODO: from unittest.mock import patch
    # with patch("requests.get") as mock_get:
    #     mock_get.return_value.json.return_value = {"name": "Alice"}
    #     result = fetch_user_from_api(1)
    #     assert result["name"] == "Alice"
    pass


# Exercise 5.C.3 — Fixture Composition
# @pytest.fixture
# def db():
#     """Fixture: test database."""
#     pass
#
# @pytest.fixture
# def user(db):
#     """Fixture: depends on db fixture."""
#     pass
#
# @pytest.fixture
# def auth_token(user):
#     """Fixture: depends on user fixture."""
#     pass


# Exercise 5.C.6 — TDD: Password Validator
class PasswordValidator:
    """Build this class using TDD — write tests first!"""

    def __init__(self, min_length=8, require_upper=True, require_digit=True, require_special=False):
        # TODO: Store rules
        pass

    def validate(self, password: str) -> tuple[bool, list[str]]:
        """Return (is_valid, list_of_errors)."""
        # TODO: Check each rule, collect error messages
        pass


# Tests for TDD (write these FIRST, then implement the class)
def test_validator_rejects_short():
    # TODO: v = PasswordValidator(min_length=8)
    # valid, errors = v.validate("Short1")
    # assert not valid
    # assert "too short" in errors[0].lower()
    pass


def test_validator_rejects_no_uppercase():
    # TODO: Implement
    pass


def test_validator_rejects_no_digit():
    # TODO: Implement
    pass


def test_validator_accepts_valid():
    # TODO: Implement
    pass


# --- DEBUG LAB ---

# Exercise 5.D.1 — Test Passes Alone, Fails Together
shared_state = []  # BUG: Shared mutable state between tests!


def test_a_adds_item():
    shared_state.append("a")
    assert len(shared_state) == 1  # Passes alone, but might fail if test_b runs first


def test_b_adds_item():
    shared_state.append("b")
    assert len(shared_state) == 1  # BUG: Depends on test order!
    # TODO: Fix by using fixtures instead of global state


# Exercise 5.D.3 — Mock Not Working (wrong patch target)
# TODO: When patching, patch where it's USED, not where it's DEFINED
# BAD:  @patch("module_a.requests.get")
# GOOD: @patch("module_b.requests.get")  ← if module_b imports requests
