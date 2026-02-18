"""
Exercise 3.B.5 — Use pdb to Step Through Code
Guide: docs/python-guide/03-debugging.md

Tasks:
1. Insert breakpoint() to enter the debugger
2. Use pdb commands: n(ext), s(tep), c(ontinue), p(rint), l(ist)
3. Inspect variables at each step
4. Find the bug by stepping through

Run: python B05_pdb_walkthrough.py
"""


def build_report(data):
    """Build a summary report from data."""
    total = 0
    categories = {}

    # TODO: Add breakpoint() here to start debugging
    # breakpoint()

    for item in data:
        amount = item.get("amount", 0)
        category = item.get("category", "uncategorized")

        total += amount

        if category in categories:
            categories[category] += amount
        else:
            categories[category] = 0  # BUG: should be = amount

    report = {
        "total": total,
        "categories": categories,
        "num_items": len(data),
    }

    return report


# Test data
sample_data = [
    {"amount": 50, "category": "food"},
    {"amount": 30, "category": "transport"},
    {"amount": 20, "category": "food"},
    {"amount": 100, "category": "rent"},
    {"amount": 15, "category": "food"},
]

result = build_report(sample_data)
print(f"Total: {result['total']}")
print(f"Categories: {result['categories']}")
# Expected food total: 85, but you'll see 35 or 0
