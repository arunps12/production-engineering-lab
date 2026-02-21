"""CRUD route handlers."""

from fastapi import APIRouter, HTTPException, Query

from .schemas import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse,
    PaginatedResponse,
)
from .database import db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201, response_model=UserResponse)
async def create_user(data: UserCreate):
    """Create a new user.

    Returns 201 Created with the new user object.
    """
    return db.create(data)


@router.get("", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
):
    """List users with pagination.

    Returns 200 OK with paginated user list.
    """
    return db.list(page=page, size=size)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a single user by ID.

    Returns 200 OK or 404 Not Found.
    """
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate):
    """Full update (replace) a user.

    All fields are required. Returns 200 OK or 404 Not Found.
    PUT is idempotent: same request always produces same state.
    """
    user = db.update(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, data: UserPatch):
    """Partial update a user.

    Only provided fields are updated. Returns 200 OK or 404 Not Found.
    """
    user = db.patch(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """Delete a user.

    Returns 204 No Content or 404 Not Found.
    DELETE is idempotent: deleting already-deleted resource is the same end state.
    """
    if not db.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return None
