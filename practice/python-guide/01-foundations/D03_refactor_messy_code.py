"""
Exercise 1.D.3 — Refactor This Messy Code
Guide: docs/python-guide/01-foundations.md

This code works but is poorly written. Refactor it to be clean, readable,
and Pythonic while maintaining the same behavior.
"""


# Messy code — refactor this:
def do_stuff(x):
    res = []
    i = 0
    while i < len(x):
        if x[i] > 0:
            if x[i] % 2 == 0:
                res.append(x[i] * x[i])
            else:
                res.append(x[i])
        else:
            pass
        i = i + 1
    s = 0
    j = 0
    while j < len(res):
        s = s + res[j]
        j = j + 1
    if len(res) > 0:
        avg = s / len(res)
    else:
        avg = 0
    return {"items": res, "sum": s, "avg": avg, "count": len(res)}


# TODO: Write your clean version below
# Requirements:
# - Use for loops instead of while
# - Use list comprehensions where appropriate
# - Use built-in functions (sum, len)
# - Give meaningful variable names
# - Add type hints and docstring
# - Keep the same output format
