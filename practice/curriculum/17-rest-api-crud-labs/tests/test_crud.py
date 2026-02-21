"""Tests for CRUD operations."""


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── CREATE ──────────────────────────────────────────────

def test_create_user(client):
    r = client.post("/users", json={
        "username": "newuser",
        "email": "new@example.com",
        "full_name": "New User",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "created_at" in data


def test_create_user_invalid_email(client):
    r = client.post("/users", json={
        "username": "test",
        "email": "not-an-email",
        "full_name": "Test",
    })
    assert r.status_code == 422


def test_create_user_short_username(client):
    r = client.post("/users", json={
        "username": "ab",
        "email": "ab@example.com",
        "full_name": "Ab User",
    })
    assert r.status_code == 422


# ── READ ────────────────────────────────────────────────

def test_list_users(client):
    r = client.get("/users")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert data["total"] == 5  # seeded users


def test_list_users_pagination(client):
    r = client.get("/users?page=1&size=2")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["pages"] == 3  # 5 users / 2 per page = 3 pages


def test_get_user(client):
    r = client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["username"] == "alice"


def test_get_user_not_found(client):
    r = client.get("/users/9999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


# ── UPDATE (PUT) ────────────────────────────────────────

def test_put_user(client):
    r = client.put("/users/1", json={
        "username": "alice_updated",
        "email": "alice_new@example.com",
        "full_name": "Alice Updated",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "alice_updated"
    assert data["email"] == "alice_new@example.com"


def test_put_user_missing_field(client):
    """PUT requires all fields — missing email should fail."""
    r = client.put("/users/1", json={
        "username": "alice_updated",
        "full_name": "Alice Updated",
    })
    assert r.status_code == 422


def test_put_user_not_found(client):
    r = client.put("/users/9999", json={
        "username": "ghost",
        "email": "ghost@example.com",
        "full_name": "Ghost",
    })
    assert r.status_code == 404


# ── UPDATE (PATCH) ──────────────────────────────────────

def test_patch_user(client):
    r = client.patch("/users/1", json={"full_name": "Alice J."})
    assert r.status_code == 200
    data = r.json()
    assert data["full_name"] == "Alice J."
    assert data["username"] == "alice"  # unchanged


def test_patch_user_not_found(client):
    r = client.patch("/users/9999", json={"full_name": "Ghost"})
    assert r.status_code == 404


# ── DELETE ──────────────────────────────────────────────

def test_delete_user(client):
    r = client.delete("/users/1")
    assert r.status_code == 204

    # Verify deleted
    r = client.get("/users/1")
    assert r.status_code == 404


def test_delete_user_not_found(client):
    r = client.delete("/users/9999")
    assert r.status_code == 404


# ── IDEMPOTENCY ─────────────────────────────────────────

def test_put_idempotent(client):
    """Same PUT request produces same state."""
    payload = {
        "username": "alice_v2",
        "email": "alice_v2@example.com",
        "full_name": "Alice V2",
    }
    r1 = client.put("/users/1", json=payload)
    r2 = client.put("/users/1", json=payload)
    assert r1.status_code == 200
    assert r2.status_code == 200
    # Same state after both requests (ignoring updated_at)
    assert r1.json()["username"] == r2.json()["username"]
    assert r1.json()["email"] == r2.json()["email"]


def test_delete_idempotent_effect(client):
    """DELETE produces same end state (resource gone)."""
    r1 = client.delete("/users/1")
    assert r1.status_code == 204
    r2 = client.delete("/users/1")
    assert r2.status_code == 404  # already gone — same end state
