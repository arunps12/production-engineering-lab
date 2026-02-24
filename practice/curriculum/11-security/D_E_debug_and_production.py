"""
Section 11 — Security: Debug Lab (D1-D5) + Production Simulation (E1)
Guide: docs/curriculum/11-security-fundamentals.md
"""


# Exercise 10.D.1 — Debug: Secrets Leaked in Docker Image
# BUG: Secret visible in docker history
# Dockerfile:
#   RUN echo "SECRET=abc123" > /app/.env
# TODO: Fix with multi-stage build or Docker secrets


# Exercise 10.D.2 — Debug: JWT Token Never Expires
def create_token_BUGGY(user_id: str) -> str:
    """BUG: No expiration set!"""
    # payload = {"sub": user_id}  # Missing "exp" claim!
    # return jwt.encode(payload, SECRET_KEY)
    pass
    # TODO: Add exp claim with timedelta


# Exercise 10.D.3 — Debug: SQL Injection in Production
# Symptom: Database has entries like: '; DROP TABLE users; --
# TODO: Find all f-string/format SQL queries, convert to parameterized


# Exercise 10.D.4 — Debug: CORS Allows Everything
# BUG: allow_origins=["*"]
# TODO: Restrict to your actual frontend domain


# Exercise 10.D.5 — Debug: Sensitive Data in Logs
class LogSanitizer:
    """Redact sensitive fields from log output."""

    SENSITIVE_FIELDS = ["password", "token", "secret", "api_key", "authorization"]

    @classmethod
    def sanitize(cls, data: dict) -> dict:
        """Replace sensitive values with [REDACTED]."""
        # TODO: Recursively check keys, redact matches
        pass


# --- PRODUCTION SIMULATION ---
# Exercise 10.E.1 — Secure a Production API
# TODO (Checklist):
# [ ] Remove hardcoded secrets → env vars
# [ ] Add JWT authentication with expiry
# [ ] Add role-based authorization
# [ ] Add input validation (Pydantic)
# [ ] Add rate limiting (100 req/min/IP)
# [ ] Add security headers
# [ ] Add audit logging
# [ ] Run pip-audit
# [ ] Docker: non-root user, no secrets in layers
# [ ] Write tests for auth, RBAC, injection prevention
