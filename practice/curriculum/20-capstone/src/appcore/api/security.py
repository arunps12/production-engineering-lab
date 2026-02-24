# =============================================================================
# Section 11 — API Key Verification
# Guide: docs/curriculum/20-capstone-project.md
#
# Exercise: Implement API key verification.
#
# TODO:
# 1. Load API_KEY from environment variable
# 2. Implement verify_api_key(api_key: str) -> bool
#    - Compare securely using hmac.compare_digest
#    - Return False if API_KEY env var is not set
# =============================================================================

import hmac
import os


def verify_api_key(api_key: str) -> bool:
    """Verify an API key against the stored secret."""
    # TODO: Implement secure comparison
    pass
