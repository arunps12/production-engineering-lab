"""
Exercise 2.B.5 — Error Handling Basics
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Use try/except to handle common errors
2. Handle specific exceptions (ValueError, KeyError, TypeError)
3. Use else and finally blocks
4. Raise your own exceptions
5. Create a custom exception class
"""


# TODO: Handle division by zero


# TODO: Handle ValueError (invalid int conversion)


# TODO: Handle KeyError (missing dict key)


# TODO: Use try/except/else/finally


# TODO: Create and raise a custom exception
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the balance."""
    pass


def withdraw(balance: float, amount: float) -> float:
    """Withdraw amount from balance. Raise if insufficient."""
    # TODO: Implement with custom exception
    pass


# TODO: Test your withdraw function
