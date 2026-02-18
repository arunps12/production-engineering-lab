"""
Exercise 2.D.2 — Debug: Scope and Closure Bugs
Guide: docs/python-guide/02-core-python-skills.md

Each function has a scope or closure bug. Find and fix them.
"""


# Bug 1: Variable scope
count = 0

def increment():
    count += 1  # UnboundLocalError!
    return count


# Bug 2: Closure over loop variable
def make_multipliers():
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)  # All will use i=4!
    return multipliers


# Bug 3: Mutable default in class
class EventLog:
    def __init__(self, events=[]):  # Shared mutable default!
        self.events = events

    def add(self, event):
        self.events.append(event)


# TODO: Fix all three bugs and add tests to verify
