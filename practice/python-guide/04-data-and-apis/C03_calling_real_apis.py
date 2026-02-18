"""
Exercise 4.C.3 — Calling Real APIs
Guide: docs/python-guide/04-data-and-apis.md

Prerequisites: pip install requests

Tasks:
1. Call the GitHub API to fetch a user profile
2. Call the GitHub API to fetch repos
3. Handle 404, timeouts, and connection errors
4. Parse and display the responses
"""

import requests


def fetch_github_user(username: str) -> dict:
    """Fetch a GitHub user's public profile."""
    # TODO: Implement
    pass


def fetch_github_repos(username: str, limit: int = 5) -> list:
    """Fetch a user's public repositories."""
    # TODO: Implement
    pass


# TODO: Test with a real GitHub username
# try:
#     profile = fetch_github_user("torvalds")
#     repos = fetch_github_repos("torvalds", limit=3)
# except requests.RequestException as e:
#     print(f"Error: {e}")
