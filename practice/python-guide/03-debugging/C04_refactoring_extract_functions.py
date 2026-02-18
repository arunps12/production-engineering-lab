"""
Exercise 3.C.4 — Refactoring: Extract Functions
Guide: docs/python-guide/03-debugging.md

This monolithic function does too many things. Refactor it into
multiple small, focused functions.
"""


def process_data(raw_data):
    """
    This function does 4 things:
    1. Validates data
    2. Cleans/normalizes data
    3. Analyzes data
    4. Formats output

    Refactor into separate functions for each responsibility.
    """
    # Validate
    if not raw_data:
        return "No data"
    valid = []
    for item in raw_data:
        if isinstance(item, dict) and "name" in item and "value" in item:
            valid.append(item)

    if not valid:
        return "No valid data"

    # Clean
    cleaned = []
    for item in valid:
        cleaned.append({
            "name": item["name"].strip().lower(),
            "value": abs(float(item["value"])),
        })

    # Analyze
    total = sum(item["value"] for item in cleaned)
    average = total / len(cleaned)
    highest = max(cleaned, key=lambda x: x["value"])
    lowest = min(cleaned, key=lambda x: x["value"])

    # Format
    lines = ["=== Data Report ==="]
    lines.append(f"Items: {len(cleaned)}")
    lines.append(f"Total: {total:.2f}")
    lines.append(f"Average: {average:.2f}")
    lines.append(f"Highest: {highest['name']} ({highest['value']:.2f})")
    lines.append(f"Lowest: {lowest['name']} ({lowest['value']:.2f})")
    lines.append("===================")
    return "\n".join(lines)


# TODO: Refactor into:
# def validate_data(raw_data: list) -> list:
# def clean_data(valid_data: list) -> list:
# def analyze_data(cleaned_data: list) -> dict:
# def format_report(analysis: dict) -> str:
# def process_data(raw_data: list) -> str:   # orchestrator


# Test data
test_data = [
    {"name": "  Alpha ", "value": "42.5"},
    {"name": "Beta", "value": -15},
    {"name": "Gamma", "value": "88.3"},
    {"invalid": True},
    {"name": "Delta", "value": "23.1"},
]

print(process_data(test_data))
