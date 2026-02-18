"""
PART E — Production Simulation: Task Manager Library
Guide: docs/python-guide/02-core-python-skills.md

Build a task management library with:
1. TaskStatus enum (TODO, IN_PROGRESS, DONE, CANCELLED)
2. Task dataclass with title, description, status, created_at, tags
3. TaskManager class with add/update/filter/display methods
4. State machine: only valid transitions allowed
5. Kanban-board style display

Acceptance Criteria:
- [ ] Uses enum for status
- [ ] Uses dataclass for Task
- [ ] State machine validates transitions
- [ ] Filter by status, tag, or search term
- [ ] Formatted Kanban board display
- [ ] All classes have docstrings
- [ ] Proper error handling with custom exceptions
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional


class TaskStatus(Enum):
    """Task states."""
    # TODO: Define states
    pass


class InvalidTransitionError(Exception):
    pass


@dataclass
class Task:
    """A single task."""
    title: str
    description: str = ""
    # TODO: Add more fields (status, created_at, tags, id)

    def transition_to(self, new_status: TaskStatus):
        """Transition task to new status with validation."""
        # TODO: Implement
        pass


class TaskManager:
    """Manages a collection of tasks."""

    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, title: str, description: str = "", tags: list[str] = None) -> Task:
        """Add a new task."""
        # TODO: Implement
        pass

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        # TODO: Implement
        pass

    def update_status(self, task_id: int, new_status: TaskStatus):
        """Update a task's status."""
        # TODO: Implement
        pass

    def filter_by_status(self, status: TaskStatus) -> list[Task]:
        """Get all tasks with given status."""
        # TODO: Implement
        pass

    def filter_by_tag(self, tag: str) -> list[Task]:
        """Get all tasks with given tag."""
        # TODO: Implement
        pass

    def display_kanban(self):
        """Display tasks as a Kanban board."""
        # TODO: Implement
        pass


# TODO: Test your task manager
if __name__ == "__main__":
    tm = TaskManager()
    # Add tasks, change statuses, display kanban board
