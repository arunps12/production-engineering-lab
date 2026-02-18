"""
Exercise 5.B.1 — First Test File: Calculator Tests
Guide: docs/python-guide/05-testing-with-pytest.md

Run: pytest practice/python-guide/05-testing/B01_calculator_test.py -v
"""


# --- The module under test ---
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# --- Tests ---
def test_add():
    # TODO: assert add(2, 3) == 5
    pass


def test_subtract():
    # TODO: assert subtract(10, 4) == 6
    pass


def test_multiply():
    # TODO: assert multiply(3, 4) == 12
    pass


def test_divide():
    # TODO: assert divide(10, 2) == 5
    pass


def test_divide_by_zero():
    # TODO: with pytest.raises(ValueError):
    #     divide(1, 0)
    pass


def test_add_negative():
    # TODO: Test with negative numbers
    pass


def test_add_floats():
    # TODO: Test with floating point numbers
    pass


def test_divide_result_type():
    # TODO: Test that divide returns float
    pass
