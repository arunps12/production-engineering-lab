"""
Exercise 3.D.1 — Debug a Real-World Data Pipeline
Guide: docs/python-guide/03-debugging.md

This data pipeline has subtle bugs that only show up with edge cases.
Find and fix them all.
"""


def load_records(raw_lines):
    """Parse raw text lines into records."""
    records = []
    for line in raw_lines:
        parts = line.strip().split(",")
        if len(parts) == 3:
            records.append({
                "name": parts[0],
                "score": int(parts[1]),  # BUG: no error handling for non-int
                "category": parts[2],
            })
    return records


def calculate_percentiles(records):
    """Calculate percentile for each record."""
    scores = sorted(r["score"] for r in records)
    for record in records:
        rank = scores.index(record["score"])
        record["percentile"] = rank / len(scores) * 100  # BUG: off-by-one, division by zero
    return records


def generate_report(records):
    """Generate a summary report."""
    categories = {}
    for r in records:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r["score"])

    report = {}
    for cat, scores in categories.items():
        report[cat] = {
            "count": len(scores),
            "average": sum(scores) / len(scores),
            "max": max(scores),
            "min": min(scores),
        }
    return report


# Test with edge cases
raw = [
    "Alice,95,A",
    "Bob,87,B",
    "Charlie,xyz,A",      # Invalid score
    "Diana,92,A",
    "Eve,87,B",            # Duplicate score (affects percentile)
    "",                     # Empty line
    "Frank,100,A",
]

# TODO: Fix all bugs so this works with edge cases
# records = load_records(raw)
# records = calculate_percentiles(records)
# report = generate_report(records)
# print(report)
