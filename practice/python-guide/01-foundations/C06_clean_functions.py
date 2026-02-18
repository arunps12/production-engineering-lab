"""
Exercise 1.C.6 — Writing Clean Functions (Refactoring)
Guide: docs/python-guide/01-foundations.md

Tasks:
1. Refactor a messy function into clean, single-purpose functions
2. Apply guard clauses (early returns)
3. Use descriptive names
4. Add type hints
5. Write docstrings
"""


# Messy function to refactor:
def process(d):
    r = []
    for i in d:
        if i["age"] >= 18:
            if i["score"] > 50:
                n = i["name"].upper()
                s = i["score"] * 1.1
                if s > 100:
                    s = 100
                r.append({"name": n, "score": s, "status": "pass"})
            else:
                r.append({"name": i["name"].upper(), "score": i["score"], "status": "fail"})
    return r


# TODO: Refactor into clean, readable functions
# def is_eligible(person: dict) -> bool:
# def calculate_adjusted_score(score: float) -> float:
# def determine_status(score: float) -> str:
# def process_candidates(candidates: list[dict]) -> list[dict]:
