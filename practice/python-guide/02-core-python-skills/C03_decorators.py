"""
Exercise 2.C.3 — Decorators
Guide: docs/python-guide/02-core-python-skills.md

Tasks:
1. Write a timer decorator that prints execution time
2. Write a retry decorator that retries on exception
3. Write a validate_types decorator
4. Understand functools.wraps
5. Stack multiple decorators
"""

import functools
import time


def timer(func):
    """Decorator that prints how long a function takes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: Implement timing logic
        pass
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator that retries a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Implement retry logic
            pass
        return wrapper
    return decorator


def validate_types(**expected_types):
    """Decorator that validates argument types."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Implement type validation
            pass
        return wrapper
    return decorator


# TODO: Test your decorators
@timer
def slow_function():
    time.sleep(0.1)
    return "done"


@retry(max_attempts=3, delay=0.1)
def flaky_function():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Random failure")
    return "success"


# TODO: Call and test
