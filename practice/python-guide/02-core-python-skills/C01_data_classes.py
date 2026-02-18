"""
Exercise 2.C.1 — Data Classes (Modern Python OOP)
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Create a dataclass for Point(x, y)
2. Create a dataclass with default values
3. Use field() for complex defaults
4. Add custom methods to a dataclass
5. Use frozen=True for immutable data
"""

from dataclasses import dataclass, field


# TODO: Basic dataclass
@dataclass
class Point:
    # TODO: Define fields
    pass


# TODO: Dataclass with defaults
@dataclass
class Config:
    # TODO: Define fields with defaults
    pass


# TODO: Frozen (immutable) dataclass
@dataclass(frozen=True)
class Color:
    # TODO: Define fields
    pass


# TODO: Test creating instances, comparing, and printing
