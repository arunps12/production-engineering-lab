"""
Exercise 5.B.4 — Parametrize Tests
Guide: docs/python-guide/05-testing-with-pytest.md
"""
import pytest


# Temperature converter functions
def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


# TODO: Use @pytest.mark.parametrize
# @pytest.mark.parametrize("fahrenheit,expected_celsius", [
#     (32, 0),
#     (212, 100),
#     (-40, -40),
#     (98.6, 37),
# ])
def test_f_to_c():
    # TODO: Parametrize this test
    pass


# Password validator
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


# TODO: Parametrize with valid and invalid passwords
# @pytest.mark.parametrize("password,expected", [
#     ("Short1A", False),       # Too short
#     ("alllowercase1", False), # No uppercase
#     ("NoDigitsHere", False),  # No digit
#     ("ValidPass1", True),     # Valid
# ])
def test_validate_password():
    # TODO: Parametrize this test
    pass
