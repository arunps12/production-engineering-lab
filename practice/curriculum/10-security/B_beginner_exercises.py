"""
Section 10 — Security: Beginner Exercises (B1-B7)
Guide: docs/curriculum/10-security-fundamentals.md
"""
import os


# Exercise 10.B.1 — Environment Variables for Secrets
class Config:
    """Application configuration from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    API_KEY = os.environ.get("API_KEY")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

    @classmethod
    def validate(cls):
        """Validate all required configuration is set."""
        # TODO: Raise ValueError if SECRET_KEY is default
        # TODO: Raise ValueError if API_KEY is None
        pass


# Exercise 10.B.3 — Input Validation
# from pydantic import BaseModel, Field, validator
# import re

# class UserCreate(BaseModel):
#     username: str = Field(min_length=3, max_length=50)
#     email: str
#     password: str = Field(min_length=8)
#
#     @validator("email")
#     def validate_email(cls, v):
#         # TODO: Validate email format with regex
#         pass
#
#     @validator("username")
#     def validate_username(cls, v):
#         # TODO: Only alphanumeric and underscore
#         pass


# Exercise 10.B.4 — SQL Injection Prevention
def get_user_UNSAFE(username: str):
    """BAD — Vulnerable to SQL injection."""
    # query = f"SELECT * FROM users WHERE username = '{username}'"
    # cursor.execute(query)
    pass


def get_user_SAFE(username: str):
    """GOOD — Parameterized query."""
    # cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    pass


# Exercise 10.B.5 — Password Hashing
def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # TODO: pip install bcrypt
    # import bcrypt
    # salt = bcrypt.gensalt()
    # return bcrypt.hashpw(password.encode(), salt).decode()
    pass


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash."""
    # TODO: return bcrypt.checkpw(password.encode(), hashed.encode())
    pass


# Exercise 10.B.7 — Dependency Vulnerability Scanning
# TODO: Run in terminal:
# pip install pip-audit
# pip-audit
