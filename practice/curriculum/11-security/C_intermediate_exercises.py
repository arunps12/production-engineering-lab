"""
Section 11 — Security: Intermediate Exercises (C1-C6)
Guide: docs/curriculum/11-security-fundamentals.md
"""


# Exercise 11.C.1 — JWT Authentication in FastAPI
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# import jwt
# from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_token(user_id: str, role: str) -> str:
    """Create a JWT token."""
    # TODO: payload = {"sub": user_id, "role": role, "exp": ...}
    # TODO: return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    pass


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token."""
    # TODO: return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # TODO: Handle ExpiredSignatureError, InvalidTokenError
    pass


# Exercise 11.C.2 — Role-Based Access Control (RBAC)
def require_role(*allowed_roles):
    """Decorator to restrict endpoint access by role."""
    # TODO: Check token role against allowed_roles
    # TODO: Raise 403 if not permitted
    pass


# Exercise 11.C.3 — Rate Limiting
class RateLimiter:
    """In-memory rate limiter."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        # TODO: self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limit."""
        # TODO: Remove old requests, check count
        pass


# Exercise 11.C.5 — Security Headers Middleware
# @app.middleware("http")
# async def add_security_headers(request, call_next):
#     response = await call_next(request)
#     # TODO: Add X-Content-Type-Options, X-Frame-Options, etc.
#     return response


# Exercise 11.C.6 — Audit Logging
def log_auth_event(event_type: str, user_id: str, ip: str, success: bool):
    """Log security-relevant events."""
    # TODO: Log with structured format (JSON)
    pass
