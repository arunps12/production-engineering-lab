"""
Section 3 — REST API Design: Advanced Debug & Production Simulation
Guide: docs/curriculum/03-rest-api-design.md

Exercise 3.D.1 — API Returns 200 for Everything
Exercise 3.D.2 — Inconsistent API Responses
"""


# Exercise 3.D.1 — API Returns 200 for Everything (BAD)
# This anti-pattern returns 200 with error info in the body.
# TODO: Fix to use proper HTTP status codes.

def bad_api_handler(request):
    """BAD: Always returns 200."""
    try:
        result = process(request)
        return {"status": 200, "data": result}
    except NotFoundError:
        return {"status": 404, "error": "Not found"}  # Still HTTP 200!
    except Exception as e:
        return {"status": 500, "error": str(e)}  # Still HTTP 200!


# TODO: Rewrite to use proper HTTP responses


# Exercise 3.D.2 — Inconsistent API Responses
# Different endpoints return data in different formats.
# TODO: Create a consistent response wrapper.

# Inconsistent:
# GET /users     → [{"name": "Alice"}, ...]
# GET /users/1   → {"user": {"name": "Alice"}}
# GET /products  → {"results": [...], "count": 10}

# TODO: Design a consistent format like:
# {"data": ..., "meta": {"total": N, "page": P}}
