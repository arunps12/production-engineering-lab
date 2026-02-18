"""
Exercise 2.C.2 — Magic Methods (Dunder Methods)
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Create a Money class with amount and currency
2. Implement __add__ for money + money
3. Implement __eq__ and __lt__ for comparison
4. Implement __repr__ and __str__
5. Implement __bool__ (truthy when amount > 0)
"""


class Money:
    """Money with currency support."""

    def __init__(self, amount: float, currency: str = "USD"):
        # TODO: Implement
        pass

    def __add__(self, other):
        # TODO: Add two Money objects (same currency only)
        pass

    def __sub__(self, other):
        # TODO: Subtract
        pass

    def __eq__(self, other):
        # TODO: Compare equality
        pass

    def __lt__(self, other):
        # TODO: Less than comparison
        pass

    def __bool__(self):
        # TODO: True when amount > 0
        pass

    def __repr__(self):
        # TODO: Developer-friendly representation
        pass

    def __str__(self):
        # TODO: User-friendly representation
        pass


# TODO: Test all operations
