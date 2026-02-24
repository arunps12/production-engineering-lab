"""In-memory database for the CRUD API."""

import math
from datetime import datetime, timezone
from .schemas import UserCreate, UserUpdate, UserPatch, UserResponse, PaginatedResponse


class InMemoryDB:
    """Simple in-memory user store."""

    def __init__(self):
        self._users: dict[int, dict] = {}
        self._next_id: int = 1
        self._seed()

    def _seed(self):
        """Seed with sample data."""
        samples = [
            ("alice", "alice@example.com", "Alice Johnson"),
            ("bob", "bob@example.com", "Bob Smith"),
            ("charlie", "charlie@example.com", "Charlie Brown"),
            ("diana", "diana@example.com", "Diana Prince"),
            ("eve", "eve@example.com", "Eve Davis"),
        ]
        for username, email, full_name in samples:
            self.create(UserCreate(username=username, email=email, full_name=full_name))

    def create(self, data: UserCreate) -> UserResponse:
        now = datetime.now(timezone.utc)
        user = {
            "id": self._next_id,
            "username": data.username,
            "email": data.email,
            "full_name": data.full_name,
            "created_at": now,
            "updated_at": now,
        }
        self._users[self._next_id] = user
        self._next_id += 1
        return UserResponse(**user)

    def get(self, user_id: int) -> UserResponse | None:
        user = self._users.get(user_id)
        return UserResponse(**user) if user else None

    def list(self, page: int = 1, size: int = 10) -> PaginatedResponse:
        all_users = sorted(self._users.values(), key=lambda u: u["id"])
        total = len(all_users)
        pages = max(1, math.ceil(total / size))
        start = (page - 1) * size
        end = start + size
        items = [UserResponse(**u) for u in all_users[start:end]]
        return PaginatedResponse(
            items=items, total=total, page=page, size=size, pages=pages
        )

    def update(self, user_id: int, data: UserUpdate) -> UserResponse | None:
        if user_id not in self._users:
            return None
        user = self._users[user_id]
        user["username"] = data.username
        user["email"] = data.email
        user["full_name"] = data.full_name
        user["updated_at"] = datetime.now(timezone.utc)
        return UserResponse(**user)

    def patch(self, user_id: int, data: UserPatch) -> UserResponse | None:
        if user_id not in self._users:
            return None
        user = self._users[user_id]
        patch_data = data.model_dump(exclude_unset=True)
        for key, value in patch_data.items():
            user[key] = value
        user["updated_at"] = datetime.now(timezone.utc)
        return UserResponse(**user)

    def delete(self, user_id: int) -> bool:
        if user_id not in self._users:
            return False
        del self._users[user_id]
        return True

    def reset(self):
        """Reset database (for testing)."""
        self._users.clear()
        self._next_id = 1
        self._seed()


# Singleton instance
db = InMemoryDB()
