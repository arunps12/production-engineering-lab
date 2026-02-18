"""
Exercise 2.C.4 — Enum and Type Safety
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Create a Status enum (PENDING, IN_PROGRESS, COMPLETED, CANCELLED)
2. Create an Order class that uses the enum for state management
3. Implement valid transitions (state machine)
4. Prevent invalid transitions
5. Use enum for type-safe comparisons
"""

from enum import Enum, auto


class OrderStatus(Enum):
    """Order status states."""
    # TODO: Define states
    pass


class InvalidTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class Order:
    """Order with state machine."""

    # Define valid transitions
    VALID_TRANSITIONS = {
        # TODO: Map each status to its allowed next statuses
    }

    def __init__(self, order_id: str):
        # TODO: Initialize
        pass

    def transition_to(self, new_status: OrderStatus):
        """Transition to a new status. Raise if invalid."""
        # TODO: Implement with validation
        pass

    def __str__(self):
        # TODO: Implement
        pass


# TODO: Test valid and invalid transitions
