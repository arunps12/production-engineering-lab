"""
PART E — Production Simulation: Debug a "Working" but Wrong Application
Guide: docs/python-guide/03-debugging.md

This application RUNS without errors but produces WRONG results.
Find and fix all the bugs.

Bugs to find:
1. Floating point addition error in financial calculations
2. Empty list edge case in statistics
3. Percentage rounding error
"""


def calculate_invoice(items):
    """Calculate invoice total. Has floating point bug."""
    total = 0.0
    for item in items:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
    # BUG: Floating point accumulation error
    # e.g., 0.1 + 0.2 = 0.30000000000000004
    return total


def get_statistics(values):
    """Calculate mean, median, mode. Has empty list bug."""
    # BUG: No handling for empty list
    mean = sum(values) / len(values)

    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 0:
        median = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    else:
        median = sorted_vals[n // 2]

    # BUG: Mode calculation only finds first occurrence
    from collections import Counter
    counts = Counter(values)
    mode = counts.most_common(1)[0][0]

    return {"mean": mean, "median": median, "mode": mode}


def calculate_percentages(counts):
    """Calculate percentages from a dict of counts. Has rounding bug."""
    total = sum(counts.values())
    percentages = {}
    for key, count in counts.items():
        percentages[key] = round(count / total * 100)
    # BUG: Rounded percentages might not sum to 100
    return percentages


# TODO: Fix all three bugs
# Test:
items = [
    {"name": "Widget", "price": 19.99, "quantity": 3},
    {"name": "Gadget", "price": 9.99, "quantity": 5},
    {"name": "Doohickey", "price": 4.99, "quantity": 10},
]
print(f"Invoice total: ${calculate_invoice(items):.2f}")

scores = [85, 92, 78, 92, 88, 90, 85]
print(f"Stats: {get_statistics(scores)}")

survey = {"agree": 47, "disagree": 32, "neutral": 21}
pcts = calculate_percentages(survey)
print(f"Percentages: {pcts} (sum: {sum(pcts.values())}%)")
