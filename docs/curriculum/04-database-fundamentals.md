# SECTION 4 — DATABASE FUNDAMENTALS FOR DEVOPS

---

## PART A — CONCEPT EXPLANATION

### Why Every DevOps Engineer Needs Database Knowledge

You will encounter databases in every production system. You need to understand:
- **How to connect and query** — Debugging data issues, verifying deployments
- **How to monitor** — Slow queries, connection pools, disk usage
- **How to back up and restore** — Disaster recovery is your responsibility
- **How to migrate** — Schema changes without downtime
- **How to containerize** — Running databases in Docker for dev/test

### Relational Databases (SQL)

Relational databases store data in **tables** (rows and columns) with **relationships** between them.

**Key concepts:**
```
Table: users
┌────┬───────────┬─────────────────┬────────────┐
│ id │ name      │ email           │ created_at │
├────┼───────────┼─────────────────┼────────────┤
│ 1  │ Alice     │ alice@test.com  │ 2025-01-01 │
│ 2  │ Bob       │ bob@test.com    │ 2025-01-02 │
└────┴───────────┴─────────────────┴────────────┘

Primary Key: id (unique identifier)
Foreign Key: References to other tables
Index: Speed up queries on specific columns
```

**ACID Properties:**
- **Atomicity** — Transaction is all-or-nothing
- **Consistency** — Database stays in valid state
- **Isolation** — Concurrent transactions don't interfere
- **Durability** — Committed data survives crashes

### SQL Essentials

```sql
-- Create
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@test.com');

-- Read
SELECT * FROM users WHERE name = 'Alice';
SELECT name, email FROM users ORDER BY created_at DESC LIMIT 10;

-- Update
UPDATE users SET email = 'new@test.com' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;

-- Join
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;
```

### Key-Value Stores (Redis)

Redis is an in-memory data store used for:
- **Caching** — Store frequently accessed data
- **Session storage** — User sessions across servers
- **Rate limiting** — Track request counts per user/IP
- **Queues** — Simple job queues with lists

```
SET user:1:name "Alice"         → OK
GET user:1:name                 → "Alice"
SETEX session:abc 3600 "data"   → Expires in 1 hour
INCR rate:192.168.1.1           → Atomic increment
LPUSH queue:jobs "job1"         → Push to queue
RPOP queue:jobs                 → Pop from queue
```

### Connection Pooling

Opening a new database connection is expensive (~50-100ms). Connection pools maintain a set of reusable connections:

```
Application ──→ Connection Pool ──→ Database
                 [conn1] ────────→
                 [conn2] ────────→  PostgreSQL
                 [conn3] ────────→
                 [conn4] (idle)
```

**Why it matters**: Without pooling, 1000 requests = 1000 connections = database dies.

### Database Migrations

Schema changes must be versioned and reproducible:

```
migrations/
├── 001_create_users.sql
├── 002_add_email_index.sql
├── 003_create_orders.sql
└── 004_add_user_role.sql
```

Tools: Alembic (Python/SQLAlchemy), Flyway, golang-migrate

### Common Beginner Misunderstandings

1. **"Just use SELECT *"** — Always specify columns. `SELECT *` is slow, fragile, and exposes unnecessary data.
2. **"Indexes make everything faster"** — Indexes speed up reads but slow down writes. Index strategically.
3. **"Redis replaces a database"** — Redis is a cache/store, not a primary database. Data can be lost on restart (unless configured for persistence).
4. **"ORMs mean I don't need SQL"** — ORMs generate SQL. When queries are slow, you need to understand the SQL underneath.
5. **"Backups are someone else's problem"** — If you deploy it, you own the backup strategy.

---

## PART B — BEGINNER PRACTICE

### Exercise 9.B.1 — SQLite Basics with Python

Use Python's built-in `sqlite3` to create a database, table, and run queries:
```python
import sqlite3
conn = sqlite3.connect("practice.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@test.com"))
conn.commit()
for row in cursor.execute("SELECT * FROM users"):
    print(row)
conn.close()
```

### Exercise 9.B.2 — CRUD Operations

Implement all four operations (Create, Read, Update, Delete) for a `tasks` table with columns: `id`, `title`, `completed`, `created_at`.

### Exercise 9.B.3 — SQL Queries Practice

Write queries for:
1. Select all incomplete tasks
2. Count tasks per completion status
3. Find the most recently created task
4. Update all tasks created before a date to completed
5. Delete completed tasks older than 30 days

### Exercise 9.B.4 — PostgreSQL with Docker

Run PostgreSQL in Docker and connect:
```bash
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=practice \
  -p 5432:5432 \
  postgres:16

# Connect with psql
docker exec -it postgres psql -U postgres -d practice
```

### Exercise 9.B.5 — Redis Basics

Run Redis in Docker and practice commands:
```bash
docker run -d --name redis -p 6379:6379 redis:7

# Connect with redis-cli
docker exec -it redis redis-cli

# Basic commands
SET greeting "hello"
GET greeting
SETEX temp_key 60 "expires in 60s"
TTL temp_key
DEL greeting
```

### Exercise 9.B.6 — Redis with Python

```python
# pip install redis
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set("user:1:name", "Alice")
print(r.get("user:1:name"))
r.setex("session:abc", 3600, "session_data")
print(r.ttl("session:abc"))
```

### Exercise 9.B.7 — Database Connection with Context Manager

Write a Python context manager for database connections:
```python
class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 9.C.1 — Connection Pooling

Implement a simple connection pool for SQLite:
```python
from queue import Queue
import sqlite3

class ConnectionPool:
    def __init__(self, db_path, size=5):
        self.pool = Queue(maxsize=size)
        for _ in range(size):
            self.pool.put(sqlite3.connect(db_path))
    
    def get_connection(self):
        return self.pool.get()
    
    def return_connection(self, conn):
        self.pool.put(conn)
```

### Exercise 9.C.2 — Database Migrations

Create a migration system:
1. Store migration files in `migrations/` directory
2. Track which migrations have been applied in a `schema_migrations` table
3. Apply pending migrations in order
4. Support rollback

### Exercise 9.C.3 — Indexing and Query Performance

```sql
-- Create a table with 100K rows
-- Query without index, measure time
-- Add index, measure again
CREATE INDEX idx_users_email ON users(email);
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'alice@test.com';
```

### Exercise 9.C.4 — Redis Caching Pattern

Implement the cache-aside pattern:
```python
def get_user(user_id):
    # 1. Check cache
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    # 2. Query database
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    # 3. Store in cache (expire in 5 min)
    redis.setex(f"user:{user_id}", 300, json.dumps(user))
    return user
```

### Exercise 9.C.5 — Redis Rate Limiter

Implement rate limiting with Redis:
```python
def is_rate_limited(client_ip, max_requests=100, window=60):
    key = f"rate:{client_ip}"
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, window)
    return current > max_requests
```

### Exercise 9.C.6 — Database Backup and Restore

```bash
# PostgreSQL backup
docker exec postgres pg_dump -U postgres practice > backup.sql

# PostgreSQL restore
docker exec -i postgres psql -U postgres practice < backup.sql

# SQLite backup (just copy the file, or use .backup command)
sqlite3 practice.db ".backup backup.db"
```

### Exercise 9.C.7 — Docker Compose with Database

Create a `docker-compose.yml` that runs your FastAPI app + PostgreSQL + Redis:
```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    depends_on: [postgres, redis]
    environment:
      DATABASE_URL: postgresql://postgres:secret@postgres:5432/app
      REDIS_URL: redis://redis:6379
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
  redis:
    image: redis:7
volumes:
  pgdata:
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 9.D.1 — Debug: Connection Pool Exhaustion

Symptom: Application hangs, then "too many connections" error.
Cause: Connections acquired but never returned to the pool.
Task: Find the missing `return_connection()` or unclosed connection.

### Exercise 9.D.2 — Debug: Slow Query

Symptom: API endpoint takes 5 seconds.
Task: Use `EXPLAIN ANALYZE` to find the slow query, add an index, verify improvement.

### Exercise 9.D.3 — Debug: Migration Failed Midway

Symptom: Table partially created, migration marked as not applied.
Task: Manually inspect database state, fix the schema, mark migration as applied.

### Exercise 9.D.4 — Debug: Redis Cache Stampede

Symptom: When a popular cache key expires, 1000 requests all hit the database simultaneously.
Task: Implement cache stampede prevention (lock-based or probabilistic early expiry).

### Exercise 9.D.5 — Debug: Data Lost After Container Restart

Symptom: PostgreSQL container restarted, all data is gone.
Cause: No volume mount — data was in the container's ephemeral filesystem.
Task: Add a Docker volume for `/var/lib/postgresql/data`.

---

## PART E — PRODUCTION SIMULATION

### Scenario: Production Database Operations

You're responsible for the database layer of a production service:

1. **Set up** PostgreSQL and Redis in Docker Compose with persistent volumes
2. **Create schema** with migrations (users, predictions, audit_log tables)
3. **Implement** connection pooling in your FastAPI app
4. **Add caching** — Cache prediction results in Redis for 5 minutes
5. **Add rate limiting** — Limit to 100 requests/minute per IP using Redis
6. **Set up backups** — Automated daily backup script with retention
7. **Monitor** — Track connection pool usage, query latency, cache hit ratio
8. **Test failover** — What happens when Redis goes down? (App should still work, just slower)

---

## Key Takeaways

1. **SQL is a must-know skill** — Even with ORMs, you need to understand queries, joins, and indexes.
2. **Always use connection pooling** — Direct connections per request will kill your database.
3. **Redis is infrastructure** — Use it for caching, sessions, and rate limiting, not as a primary database.
4. **Migrations must be versioned** — Never manually modify production schemas.
5. **Volumes are critical** — Database containers without volumes lose all data on restart.
6. **Backups are your responsibility** — Test restores regularly, not just backups.

---
*Next: [Section 5 — REST API Design](05-rest-api-design.md)*
