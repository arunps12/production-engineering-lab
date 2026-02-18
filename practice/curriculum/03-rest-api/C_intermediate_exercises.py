"""
Section 3 — REST API Design: Intermediate Practice
Guide: docs/curriculum/03-rest-api-design.md

Exercise 3.C.1 — Refactor a Broken API
Exercise 3.C.3 — Pagination Design
Exercise 3.C.4 — Error Handling Strategy
"""


# Exercise 3.C.1 — Refactor a Broken API
# This API has design problems. Identify and fix them.
# Bad endpoints:
#   POST /getUsers          → should be GET /users
#   GET /deleteUser/123     → should be DELETE /users/123
#   PUT /user               → should be PUT /users/123
#   GET /api/v1/users/list  → should be GET /api/v1/users

# TODO: Write the corrected endpoint signatures


# Exercise 3.C.3 — Pagination Design
# TODO: Design pagination parameters (page, per_page, cursor)
# TODO: Design pagination response (items, total, next_page, prev_page)


# Exercise 3.C.4 — Error Handling Strategy
# TODO: Design consistent error response format
# TODO: Map exceptions to status codes
