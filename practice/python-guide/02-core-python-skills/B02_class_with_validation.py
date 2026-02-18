"""
Exercise 2.B.2 — Class with Validation
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Create a Temperature class with celsius value
2. Validate temperature on creation (>= -273.15)
3. Add @classmethod for from_fahrenheit()
4. Add @property for fahrenheit conversion
5. Make it impossible to set invalid temperatures
"""


class Temperature:
    """Temperature with validation and unit conversion."""

    def __init__(self, celsius: float):
        # TODO: Validate and store
        pass

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        """Create Temperature from Fahrenheit value."""
        # TODO: Implement
        pass

    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        # TODO: Implement
        pass

    def __str__(self) -> str:
        # TODO: Implement
        pass


# TODO: Test valid and invalid temperatures
