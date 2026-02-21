# Module 14 — PostgreSQL Production Labs

## Goals

- Run PostgreSQL in Docker and connect with `psql`
- Design relational schemas with constraints and indexes
- Debug slow queries using `EXPLAIN ANALYZE`
- Understand transactions, locks, and isolation levels
- Manage schema migrations with Alembic in a production-style workflow

## Prerequisites

- Docker & Docker Compose installed
- Python 3.11+ with `uv`
- Completed modules 0–5 (basic Linux, networking, Docker knowledge)

## Setup

```bash
cd practice/curriculum/14-postgresql-production-labs
docker compose up -d
```

Wait for Postgres to be ready:

```bash
docker compose exec postgres pg_isready -U labuser
# Expected: /var/run/postgresql:5432 - accepting connections
```

---

## Exercise 14.1 — Run Postgres in Docker + Connect

### Objective

Start a Postgres container, connect via `psql`, create a database, user, and grant privileges.

### Steps

1. Start the stack:

```bash
docker compose up -d
```

2. Connect to Postgres:

```bash
docker compose exec postgres psql -U labuser -d labdb
```

3. Run the setup script:

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/ex14_1_setup.sql
```

4. Verify:

```bash
docker compose exec postgres psql -U labuser -d labdb -c "\du"
docker compose exec postgres psql -U labuser -d labdb -c "\l"
docker compose exec postgres psql -U labuser -d labdb -c "SELECT current_user, current_database();"
```

### Expected Output

```
 current_user | current_database
--------------+------------------
 labuser      | labdb
```

### Deliverables

- [scripts/ex14_1_setup.sql](scripts/ex14_1_setup.sql) — role/database creation script

---

## Exercise 14.2 — Schema Design (users / projects / tasks / audit_logs)

### Objective

Design a normalized schema with constraints, indexes, sample data, and write JOIN + aggregation queries.

### Steps

1. Create the schema:

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/schema.sql
```

2. Seed sample data:

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/seed.sql
```

3. Run queries:

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/queries.sql
```

### Verification

```bash
docker compose exec postgres psql -U labuser -d labdb -c "\dt"
```

Expected tables: `users`, `projects`, `tasks`, `audit_logs`

```bash
docker compose exec postgres psql -U labuser -d labdb -c "\di"
```

Expected indexes: primary keys + `idx_tasks_project_id`, `idx_tasks_status_priority`, `idx_audit_logs_entity`, `idx_users_email`

### Deliverables

- [scripts/schema.sql](scripts/schema.sql) — full DDL
- [scripts/seed.sql](scripts/seed.sql) — sample data
- [scripts/queries.sql](scripts/queries.sql) — JOIN and aggregation queries

---

## Exercise 14.3 — Performance Debugging

### Objective

Insert 100k rows, identify a slow query, use `EXPLAIN ANALYZE`, add an index, and compare execution plans.

### Steps

1. Generate bulk data:

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/generate_bulk_data.sql
```

2. Run the slow query and capture the plan:

```bash
docker compose exec postgres psql -U labuser -d labdb -c "
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT t.title, u.username, p.name as project_name
FROM tasks t
JOIN users u ON t.assigned_to = u.id
JOIN projects p ON t.project_id = p.id
WHERE t.status = 'pending' AND t.priority > 3
ORDER BY t.created_at DESC
LIMIT 50;
"
```

3. Note the execution time (Seq Scan expected).

4. Add targeted indexes:

```bash
docker compose exec postgres psql -U labuser -d labdb -c "
CREATE INDEX IF NOT EXISTS idx_tasks_status_priority_created
ON tasks (status, priority, created_at DESC);
"
```

5. Re-run EXPLAIN ANALYZE and compare.

6. Check index usage stats:

```bash
docker compose exec postgres psql -U labuser -d labdb -c "
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
"
```

### Deliverables

- [scripts/generate_bulk_data.sql](scripts/generate_bulk_data.sql) — bulk insert script
- [solutions/benchmark.md](solutions/benchmark.md) — reference EXPLAIN output and analysis

---

## Exercise 14.4 — Transactions, Locks & Isolation Levels

### Objective

Demonstrate transaction isolation, lock contention, and a safe deadlock scenario.

### Steps

Open **two** terminal sessions (Session A and Session B).

#### Part 1 — Read Committed vs Repeatable Read

**Session A:**

```sql
-- Session A: Start transaction with READ COMMITTED (default)
BEGIN;
SELECT balance FROM accounts WHERE id = 1;
-- Note the value
```

**Session B:**

```sql
-- Session B: Update the same row and commit
BEGIN;
UPDATE accounts SET balance = balance + 100 WHERE id = 1;
COMMIT;
```

**Session A:**

```sql
-- Session A: Read again — you will see Session B's committed change
SELECT balance FROM accounts WHERE id = 1;
COMMIT;
```

Now repeat with `REPEATABLE READ`:

**Session A:**

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;
```

**Session B:**

```sql
BEGIN;
UPDATE accounts SET balance = balance + 100 WHERE id = 1;
COMMIT;
```

**Session A:**

```sql
-- Session A: Read again — same value as first read (snapshot isolation)
SELECT balance FROM accounts WHERE id = 1;
COMMIT;
```

#### Part 2 — Lock Contention

**Session A:**

```sql
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
-- Do NOT commit yet
```

**Session B:**

```sql
BEGIN;
-- This will BLOCK waiting for Session A's lock
UPDATE accounts SET balance = balance + 25 WHERE id = 1;
```

**Session A:**

```sql
COMMIT; -- Now Session B unblocks
```

**Session B:**

```sql
COMMIT;
```

#### Part 3 — Safe Deadlock Demo

**Session A:**

```sql
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
```

**Session B:**

```sql
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 2;
```

**Session A:**

```sql
-- This will wait for Session B's lock on id=2
UPDATE accounts SET balance = balance + 10 WHERE id = 2;
```

**Session B:**

```sql
-- This causes a deadlock — Postgres detects and aborts one transaction
UPDATE accounts SET balance = balance + 10 WHERE id = 1;
-- ERROR: deadlock detected
```

Check Postgres logs:

```bash
docker compose logs postgres | grep -i deadlock
```

### Setup for this exercise

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/transactions_setup.sql
```

### Deliverables

- [scripts/transactions_setup.sql](scripts/transactions_setup.sql) — accounts table setup
- [solutions/transactions_lab.md](solutions/transactions_lab.md) — reference walkthrough

---

## Exercise 14.5 — Alembic Migrations (Production Workflow)

### Objective

Use Alembic with SQLAlchemy to manage schema migrations in a production-style workflow.

### Steps

1. Set up the mini app:

```bash
cd alembic_lab
uv sync
```

2. Initialize Alembic (already done — review the config):

```bash
ls alembic/ alembic.ini
```

3. Create a new migration revision:

```bash
uv run alembic revision --autogenerate -m "add_articles_table"
```

4. Review the generated migration in `alembic/versions/`.

5. Apply the migration:

```bash
uv run alembic upgrade head
```

6. Check current revision:

```bash
uv run alembic current
```

7. Downgrade one step:

```bash
uv run alembic downgrade -1
```

8. Upgrade back:

```bash
uv run alembic upgrade head
```

9. View migration history:

```bash
uv run alembic history --verbose
```

### Common Failures & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| `Target database is not up to date` | Branch divergence | `alembic merge heads -m "merge"` |
| `Can't locate revision` | Missing migration file | Check `alembic/versions/` directory |
| `relation already exists` | Migration applied outside Alembic | `alembic stamp head` to sync state |
| Connection refused | Postgres not running | `docker compose up -d` |

### Deliverables

- [alembic_lab/](alembic_lab/) — complete mini-app with working Alembic setup

---

## Cleanup

```bash
docker compose down -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `psql: connection refused` | Ensure Postgres container is running: `docker compose ps` |
| `FATAL: role "labuser" does not exist` | Restart compose: `docker compose down -v && docker compose up -d` |
| Permission denied on volume | `sudo chown -R $(id -u):$(id -g) ./data/` |
| Slow EXPLAIN ANALYZE | Increase `shared_buffers` in compose environment |

## Next Steps

- Module 15: Elasticsearch Practice
- Module 17: REST API CRUD Labs (uses Postgres)
