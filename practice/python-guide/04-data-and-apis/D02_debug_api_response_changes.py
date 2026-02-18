"""
Exercise 4.D.2 — Debug: API Response Changes
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. See how the fragile parser breaks on API changes
2. Build a robust parser that handles multiple response formats
3. Use .get() with fallbacks instead of direct key access
"""


def process_api_response_fragile(data):
    """FRAGILE: Assumes exact structure. Will break easily."""
    return {
        "id": data["results"][0]["id"],
        "name": data["results"][0]["name"],
        "email": data["results"][0]["email"],
    }


def process_api_response_robust(data):
    """ROBUST: Handle structure changes gracefully."""
    # TODO: Implement with .get(), fallback keys, empty checks
    pass


# Test with different API response versions
v1_response = {"results": [{"id": 1, "name": "Alice", "email": "alice@test.com"}]}
v2_response = {"data": [{"user_id": 1, "full_name": "Alice", "contact_email": "alice@test.com"}]}
v3_response = {"results": []}
v4_response = {}

# TODO: Test both parsers against all versions
