"""
Exercise 3.B.3 — Print Debugging
Guide: docs/python-guide/03-debugging.md

This function produces wrong results. Use print() statements
to trace the values at each step and find the bug.
"""


def process_scores(scores, curve=5):
    """Apply curve to scores and return stats."""
    adjusted = []
    for score in scores:
        new_score = score + curve
        if new_score > 100:
            new_score = 100
        adjusted.append(new_score)

    total = 0
    for s in adjusted:
        total = s  # BUG: should be total += s

    average = total / len(adjusted)

    passing = []
    for s in adjusted:
        if s > 60:  # Should this be >= 60?
            passing.append(s)

    return {
        "adjusted": adjusted,
        "average": average,
        "passing_count": len(passing),
        "highest": max(adjusted),
    }


# TODO: Add print() statements to trace values
# TODO: Find and fix the bugs
# TODO: Test with these scores:
scores = [55, 72, 68, 90, 45, 88, 60, 75]
result = process_scores(scores)
print(result)
