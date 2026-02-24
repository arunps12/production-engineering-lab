"""Pydantic schemas for the CRUD API."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a user (POST)."""

    username: str = Field(
        ..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$",
        description="Username (alphanumeric + underscore, 3-50 chars)",
    )
    email: EmailStr = Field(..., description="Valid email address")
    full_name: str = Field(
        ..., min_length=1, max_length=200, description="Full name"
    )


class UserUpdate(BaseModel):
    """Schema for full update (PUT) — all fields required."""

    username: str = Field(
        ..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$",
    )
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=200)


class UserPatch(BaseModel):
    """Schema for partial update (PATCH) — all fields optional."""

    username: str | None = Field(
        None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$",
    )
    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=1, max_length=200)


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int
    username: str
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime


class PaginatedResponse(BaseModel):
    """Paginated list response."""

    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    detail: str
    status_code: int
