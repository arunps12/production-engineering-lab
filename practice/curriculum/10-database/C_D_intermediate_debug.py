"""
Section 10 — Database: Intermediate (C1-C7) + Debug (D1-D5)
Guide: docs/curriculum/10-database-fundamentals.md
"""


# Exercise 10.C.1 — Connection Pool
class ConnectionPool:
    """Simple connection pool for SQLite."""

    def __init__(self, db_path: str, size: int = 5):
        # TODO: Create a queue of connections
        pass

    def get_connection(self):
        # TODO: Return a connection from the pool
        pass

    def return_connection(self, conn):
        # TODO: Return connection to the pool
        pass


# Exercise 10.C.2 — Migration System
class MigrationRunner:
    """Apply database migrations in order."""

    def __init__(self, db_path: str, migration_dir: str):
        self.db_path = db_path
        self.migration_dir = migration_dir

    def get_applied_migrations(self):
        """Check which migrations have been applied."""
        # TODO: SELECT * FROM schema_migrations
        pass

    def get_pending_migrations(self):
        """Find migration files that haven't been applied."""
        # TODO: Compare files in migration_dir with applied
        pass

    def apply(self):
        """Apply all pending migrations."""
        # TODO: Run each pending migration in order
        pass


# Exercise 10.C.4 — Cache-Aside Pattern
def get_user_cached(user_id: int):
    """Fetch user with Redis cache."""
    # TODO: 1. Check Redis cache
    # TODO: 2. If miss, query database
    # TODO: 3. Store in cache with TTL
    # TODO: 4. Return result
    pass


# Exercise 10.C.5 — Rate Limiter with Redis
def is_rate_limited(client_ip: str, max_requests: int = 100, window: int = 60) -> bool:
    """Check if client has exceeded rate limit."""
    # TODO: INCR rate:{client_ip}
    # TODO: EXPIRE on first request
    # TODO: Return True if over limit
    pass


# --- DEBUG LAB ---

# Exercise 10.D.1 — Connection Pool Exhaustion
# BUG: Connections acquired but never returned
# def process_request(pool):
#     conn = pool.get_connection()
#     result = conn.execute("SELECT ...")
#     # Missing: pool.return_connection(conn)
#     return result

# Exercise 10.D.2 — Slow Query
# TODO: Use EXPLAIN ANALYZE on a query without an index
# TODO: Add index, measure improvement

# Exercise 10.D.4 — Cache Stampede
# TODO: When cache expires, 1000 requests hit DB simultaneously
# Fix: Use lock to prevent thundering herd
