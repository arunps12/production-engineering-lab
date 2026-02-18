"""
Exercise 2.B.3 — Inheritance
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Create a base Shape class with name and color
2. Create Circle subclass with radius, override area()
3. Create Triangle subclass with base and height, override area()
4. Use super().__init__() correctly
5. Demonstrate polymorphism with a list of shapes
"""

import math


class Shape:
    """Base shape class."""

    def __init__(self, name: str, color: str = "black"):
        # TODO: Implement
        pass

    def area(self) -> float:
        """Calculate area. Must be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement area()")

    def __str__(self) -> str:
        # TODO: Implement
        pass


class Circle(Shape):
    """Circle shape."""

    def __init__(self, radius: float, color: str = "black"):
        # TODO: Call super().__init__() and store radius
        pass

    def area(self) -> float:
        # TODO: Implement
        pass


class Triangle(Shape):
    """Triangle shape."""

    def __init__(self, base: float, height: float, color: str = "black"):
        # TODO: Implement
        pass

    def area(self) -> float:
        # TODO: Implement
        pass


# TODO: Create a list of different shapes and print their areas (polymorphism)
