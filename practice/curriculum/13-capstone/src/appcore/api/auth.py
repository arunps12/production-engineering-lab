# =============================================================================
# Section 10 — FastAPI Auth Dependency
# Guide: docs/curriculum/13-capstone-project.md
#
# Exercise: Create a FastAPI dependency for API key authentication.
#
# TODO:
# 1. Create APIKeyHeader instance (header name: "X-API-Key")
# 2. Implement require_api_key dependency:
#    - Extract key from header
#    - Call verify_api_key()
#    - Raise HTTPException(403) if invalid
#    - Return the key if valid
# 3. Apply to protected routes via Depends(require_api_key)
# =============================================================================

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from appcore.api.security import verify_api_key

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str = Depends(api_key_header)) -> str:
    """FastAPI dependency that enforces API key authentication."""
    # TODO: Validate key, raise 403 if missing/invalid
    pass
