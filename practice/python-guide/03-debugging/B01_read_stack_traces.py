"""
Exercise 3.B.1 — Read These Stack Traces
Guide: docs/python-guide/03-debugging.md

Tasks:
1. Run each buggy function
2. Read the stack trace that appears
3. Identify: which file, which line, what error type, what message
4. Fix the bug
"""


# Bug 1: TypeError
def greet(name):
    return "Hello, " + name

# TODO: Call greet(42) — read the stack trace, then fix


# Bug 2: IndexError
def get_last(items):
    return items[len(items)]

# TODO: Call get_last([1,2,3]) — read the stack trace, then fix


# Bug 3: KeyError
def get_user_email(user):
    return user["email"]

# TODO: Call get_user_email({"name": "Alice"}) — read the trace, then fix


# Bug 4: AttributeError
def get_upper(text):
    return text.upper()

# TODO: Call get_upper(None) — read the trace, then fix
