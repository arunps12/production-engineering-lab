"""
Exercise 3.B.4 — Assert-Based Debugging
Guide: docs/python-guide/03-debugging.md

Tasks:
1. Add assert statements to validate function inputs
2. Add assert statements to validate intermediate results
3. Use assertions as documentation of expected behavior
"""


def calculate_bmi(weight_kg, height_m):
    """Calculate BMI. Weight in kg, height in meters."""
    # TODO: Add assertions for valid inputs
    # assert weight_kg > 0, "Weight must be positive"
    # assert 0.5 < height_m < 3.0, "Height must be realistic"

    bmi = weight_kg / (height_m ** 2)

    # TODO: Add assertion for valid output
    # assert 5 < bmi < 100, f"BMI {bmi} seems unrealistic"

    return round(bmi, 1)


def merge_sorted(list1, list2):
    """Merge two sorted lists into one sorted list."""
    # TODO: Add assertion that inputs are sorted
    # assert list1 == sorted(list1), "list1 must be sorted"
    # assert list2 == sorted(list2), "list2 must be sorted"

    result = sorted(list1 + list2)

    # TODO: Add assertion that output is sorted and correct length
    return result


# TODO: Test with valid and invalid inputs
# TODO: See what happens when assertions fail
