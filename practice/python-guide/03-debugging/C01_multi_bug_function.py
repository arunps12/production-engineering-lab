"""
Exercise 3.C.1 — Multi-Bug Function
Guide: docs/python-guide/03-debugging.md

This function has 5 bugs. Find and fix ALL of them.
The function should process a list of student records and return statistics.
"""


def analyze_students(students):
    """
    Analyze student data and return stats.

    Expected input: list of dicts with 'name', 'scores' (list of ints), 'grade'
    Expected output: dict with 'count', 'average_score', 'top_student', 'grade_distribution'
    """
    if not students:
        return None  # Bug 1: Should return empty stats dict, not None

    total_score = 0
    grade_counts = {}

    for student in students:
        scores = student["scores"]
        avg = sum(scores) / len(scores)  # Bug 2: No check for empty scores

        total_score += avg

        grade = student["grade"]
        if grade in grade_counts:
            grade_counts[grade] = +1  # Bug 3: = +1 instead of += 1
        else:
            grade_counts[grade] = 1

    average = total_score / len(students)

    # Bug 4: Crashes if scores is empty for any student
    top_student = max(students, key=lambda s: sum(s["scores"]) / len(s["scores"]))

    return {
        "count": len(students),
        "average_score": round(average),  # Bug 5: Should round to 2 decimal places
        "top_student": top_student["name"],
        "grade_distribution": grade_counts,
    }


# Test data
test_students = [
    {"name": "Alice", "scores": [85, 92, 78], "grade": "A"},
    {"name": "Bob", "scores": [72, 68, 84], "grade": "B"},
    {"name": "Charlie", "scores": [95, 98, 92], "grade": "A"},
    {"name": "Diana", "scores": [60, 55, 70], "grade": "C"},
]

# TODO: Fix all 5 bugs and verify
result = analyze_students(test_students)
print(result)
