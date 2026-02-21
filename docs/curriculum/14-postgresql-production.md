# SECTION 14 — POSTGRESQL PRODUCTION LABS

---

## PART A — CONCEPT EXPLANATION

### Why PostgreSQL?

PostgreSQL is the most advanced open-source relational database. As a production engineer you will:
- **Design schemas** — Normalize data, enforce constraints, plan indexes
- **Debug performance** — Read `EXPLAIN ANALYZE` output, identify missing indexes
- **Manage transactions** — Understand isolation levels, prevent deadlocks
- **Run migrations** — Evolve schemas safely with tools like Alembic
- **Operate in containers** — Run Postgres in Docker with proper volumes and health checks

### Relational Data Modeling

Good schema design follows **normalization** rules — eliminate duplicate data by splitting into related tables:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   users     │     │   projects   │     │     tasks        │
│─────────────│     │──────────────│     │─────────────────│
│ id (PK)     │←──┐ │ id (PK)      │←──┐ │ id (PK)         │
│ username    │   │ │ name         │   │ │ title           │
│ email       │   │ │ owner_id(FK) │───┘ │ project_id (FK) │──→ projects
│ created_at  │   │ │ created_at   │     │ assigned_to(FK) │──→ users
└─────────────┘   │ └──────────────┘     │ status          │
                  └──────────────────────│ priority        │
                                         │ created_at      │
                                         └─────────────────┘
```

**Key constraints:**
- **PRIMARY KEY** — Uniquely identifies each row
- **FOREIGN KEY** — Enforces referential integrity between tables
- **UNIQUE** — Prevents duplicate values (e.g., email)
- **NOT NULL** — Column must have a value
- **CHECK** — Custom validation (e.g., `status IN ('open','closed')`)

### Indexes — The Performance Lever

An index is a separate data structure that makes lookups fast:

```
Without index:          With index (B-tree):
┌────────────────┐      ┌───────────────┐
│ Scan ALL rows  │      │ Binary search │
│ 100,000 rows   │      │ ~17 steps     │
│ O(n)           │      │ O(log n)      │
└────────────────┘      └───────────────┘
Time: ~50ms              Time: ~0.5ms
```

**When to create indexes:**
- Columns used in `WHERE` clauses frequently
- Columns used in `JOIN` conditions
- Columns used in `ORDER BY`
- **Composite indexes** for multi-column filters: `(status, priority)`

**When NOT to create indexes:**
- Tables with few rows (< 1000)
- Columns with low cardinality (e.g., boolean `active`)
- Write-heavy tables (indexes slow down INSERTs/UPDATEs)

### EXPLAIN ANALYZE — Reading Query Plans

`EXPLAIN ANALYZE` runs the query and shows the execution plan:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT t.title, u.username
FROM tasks t
JOIN users u ON t.assigned_to = u.id
WHERE t.status = 'open'
AND t.priority >= 4;
```

**Key things to look for:**

| Term | Meaning | Good/Bad |
|------|---------|----------|
| Seq Scan | Scans every row | Bad on large tables |
| Index Scan | Uses an index | Good |
| Index Only Scan | Reads from index alone | Best |
| Bitmap Index Scan | Combines multiple indexes | Good |
| Nested Loop | Joins row-by-row | OK for small sets |
| Hash Join | Builds hash table for join | Good for large sets |
| Sort | Sorts result set | Check if index can avoid |
| Rows Removed by Filter | Rows read but discarded | Possible missing index |

**Reading the numbers:**
```
Seq Scan on tasks  (cost=0.00..1834.00 rows=5000 width=36)
                          ↑         ↑        ↑        ↑
                     startup    total    estimated   row size
                      cost      cost      rows     (bytes)
  (actual time=0.015..12.345 rows=4892 loops=1)
          ↑              ↑         ↑          ↑
      actual start   actual end  actual     iterations
        time (ms)    time (ms)    rows
```

### Transactions and Isolation Levels

A transaction groups operations into an atomic unit — all succeed or all fail (rollback):

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- both succeed, or neither does
```

**PostgreSQL isolation levels:**

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Use Case |
|-------|-----------|-------------------|-------------|----------|
| Read Uncommitted | No¹ | Yes | Yes | Rarely used |
| Read Committed (default) | No | Yes | Yes | Most applications |
| Repeatable Read | No | No | No² | Financial reporting |
| Serializable | No | No | No | Strict consistency |

¹ Postgres treats Read Uncommitted as Read Committed
² Postgres prevents phantoms at Repeatable Read level

**Lock types:**
- **Row-level locks** — `SELECT ... FOR UPDATE` locks specific rows
- **Table-level locks** — `LOCK TABLE` (avoid in production)
- **Advisory locks** — Application-defined cooperative locks

### Deadlocks

A deadlock occurs when two transactions wait for each other:

```
Transaction A:                Transaction B:
UPDATE accounts WHERE id=1;   UPDATE accounts WHERE id=2;
-- holds lock on row 1        -- holds lock on row 2
UPDATE accounts WHERE id=2;   UPDATE accounts WHERE id=1;
-- waits for row 2 (held by B)  -- waits for row 1 (held by A)
-- DEADLOCK!
```

**Prevention:** Always lock rows in a consistent order (e.g., by ascending ID).

Postgres detects deadlocks automatically and kills one transaction with:
```
ERROR: deadlock detected
```

### Schema Migrations with Alembic

Alembic tracks schema changes as versioned migration files:

```
alembic/versions/
├── 0001_initial.py          ← CREATE TABLE users, articles
├── 0002_add_tags.py         ← ALTER TABLE articles ADD tags
└── 0003_add_index.py        ← CREATE INDEX idx_articles_title
```

Each migration has `upgrade()` and `downgrade()` functions:

```python
def upgrade():
    op.add_column('articles', sa.Column('tags', sa.Text()))

def downgrade():
    op.drop_column('articles', 'tags')
```

**Commands:**
```bash
alembic revision -m "add tags"  # Create new migration
alembic upgrade head            # Apply all pending
alembic downgrade -1            # Rollback one step
alembic history                 # List all migrations
alembic current                 # Show current version
```

### Common Beginner Misunderstandings

1. **"I don't need indexes for small tables"** — True, but tables grow. Plan indexes when designing schemas.
2. **"EXPLAIN is enough"** — Use `EXPLAIN ANALYZE` to get **actual** execution times, not just estimates.
3. **"Transactions are slow"** — Every single SQL statement is already a transaction. Explicit transactions group operations for atomicity.
4. **"Just use SERIALIZABLE for everything"** — Highest isolation means highest contention. Most CRUD apps work fine with Read Committed.
5. **"Alembic auto-generates everything"** — Autogenerate is a starting point. Always review and edit generated migrations.

---

## PART B — BEGINNER PRACTICE

### Exercise 14.B.1 — Run Postgres in Docker + Connect

Start a PostgreSQL container, connect via `psql`, create users and verify the connection.

```bash
cd practice/curriculum/14-postgresql-production-labs
docker compose up -d
docker compose exec postgres psql -U labuser -d labdb
```

Run the setup script and verify:

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/ex14_1_setup.sql
docker compose exec postgres psql -U labuser -d labdb -c "SELECT current_user, current_database();"
```

**Practice file:** `practice/curriculum/14-postgresql-production-labs/scripts/ex14_1_setup.sql`

### Exercise 14.B.2 — Schema Design

Create a normalized schema with four tables (`users`, `projects`, `tasks`, `audit_logs`), seed sample data, and run JOIN + aggregation queries.

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/schema.sql
docker compose exec -T postgres psql -U labuser -d labdb < scripts/seed.sql
docker compose exec -T postgres psql -U labuser -d labdb < scripts/queries.sql
```

Verify all tables and indexes are created:

```bash
docker compose exec postgres psql -U labuser -d labdb -c "\dt"
docker compose exec postgres psql -U labuser -d labdb -c "\di"
```

**Practice files:**
- `practice/curriculum/14-postgresql-production-labs/scripts/schema.sql`
- `practice/curriculum/14-postgresql-production-labs/scripts/seed.sql`
- `practice/curriculum/14-postgresql-production-labs/scripts/queries.sql`

### Exercise 14.B.3 — Basic SQL Query Practice

Write and run these queries:

1. All tasks assigned to a specific user with project name (`JOIN`)
2. Task count grouped by status (`GROUP BY`)
3. Users with more than 2 assigned tasks (`HAVING`)
4. Tasks sorted by priority descending, then by creation date
5. Most recent audit log entries with user info

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 14.C.1 — Performance Debugging with EXPLAIN ANALYZE

Insert 100,000 rows, run a slow query, analyze the plan, add an index, and measure the improvement:

```bash
docker compose exec -T postgres psql -U labuser -d labdb < scripts/generate_bulk_data.sql
```

Run the slow query:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT t.title, u.username, p.name
FROM tasks t
JOIN users u ON t.assigned_to = u.id
JOIN projects p ON t.project_id = p.id
WHERE t.status = 'open' AND t.priority >= 4
ORDER BY t.created_at DESC
LIMIT 20;
```

Look for `Seq Scan` on `tasks`. Add the composite index:

```sql
CREATE INDEX idx_tasks_status_priority ON tasks(status, priority);
```

Run `EXPLAIN ANALYZE` again and compare execution time.

**Solution:** `practice/curriculum/14-postgresql-production-labs/solutions/benchmark.md`

### Exercise 14.C.2 — Transactions and Isolation Levels

Practice concurrent transactions using two `psql` sessions:

```bash
# Terminal 1
docker compose exec postgres psql -U labuser -d labdb

# Terminal 2
docker compose exec postgres psql -U labuser -d labdb
```

Experiment:
1. Start a transaction in T1, update a row, but don't commit
2. In T2, try to read the same row — observe Read Committed behavior
3. Try `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ` and see the difference
4. Trigger a deadlock by locking rows in opposite order

**Solution:** `practice/curriculum/14-postgresql-production-labs/solutions/transactions_lab.md`

### Exercise 14.C.3 — Audit Logging with Triggers

Create a trigger that automatically logs changes to the `audit_logs` table:

```sql
CREATE OR REPLACE FUNCTION log_task_changes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (entity_type, entity_id, action, changes)
    VALUES ('task', NEW.id, TG_OP,
            jsonb_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW)));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER task_audit_trigger
AFTER UPDATE ON tasks
FOR EACH ROW EXECUTE FUNCTION log_task_changes();
```

### Exercise 14.C.4 — Backup and Restore

```bash
# Backup
docker compose exec postgres pg_dump -U labuser labdb > backup.sql

# Restore (into a new database)
docker compose exec postgres createdb -U labuser labdb_restore
docker compose exec -T postgres psql -U labuser -d labdb_restore < backup.sql

# Verify
docker compose exec postgres psql -U labuser -d labdb_restore -c "SELECT count(*) FROM tasks;"
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 14.D.1 — Debug: Slow Query in Production

**Symptom:** An API endpoint taking 8 seconds to respond.

**Task:**
1. Connect to the database and run `pg_stat_activity` to find long-running queries
2. Use `EXPLAIN ANALYZE` on the slow query
3. Identify the missing index
4. Add the index without locking the table (`CREATE INDEX CONCURRENTLY`)
5. Verify the query is now fast

```sql
-- Find slow queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND (now() - query_start) > interval '5 seconds';
```

### Exercise 14.D.2 — Debug: Deadlock Detection

**Symptom:** Application logs show `ERROR: deadlock detected`.

**Task:**
1. Reproduce the deadlock with two concurrent transactions
2. Read the PostgreSQL log to see which transaction was killed
3. Fix the code to lock rows in consistent order
4. Verify the deadlock no longer occurs

### Exercise 14.D.3 — Debug: Connection Pool Exhaustion

**Symptom:** `FATAL: too many connections for role "labuser"`.

**Task:**
1. Check current connections: `SELECT count(*) FROM pg_stat_activity;`
2. Identify leaked connections (long-idle sessions)
3. Kill idle sessions: `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND query_start < now() - interval '10 minutes';`
4. Configure `max_connections` and implement connection pooling in your app

### Exercise 14.D.4 — Debug: Data Lost After Container Restart

**Symptom:** Postgres container restarted and all data is gone.

**Task:**
1. Check if a volume is mounted: `docker inspect <container> | jq '.[0].Mounts'`
2. If no volume — data was ephemeral
3. Add a named volume for `/var/lib/postgresql/data`
4. Restart and verify data persists across container restarts

---

## PART E — PRODUCTION SIMULATION

### Scenario: Production PostgreSQL Operations

You are the on-call engineer for a production PostgreSQL deployment:

1. **Set up** — Run Postgres in Docker with persistent volume, proper health check, and resource limits
2. **Design schema** — Create users, projects, tasks, and audit_logs with proper constraints and indexes
3. **Seed data** — Insert 100k+ rows to simulate production volume
4. **Analyze performance** — Run `EXPLAIN ANALYZE` on application queries, identify bottlenecks
5. **Add indexes** — Create indexes to bring query time from seconds to milliseconds
6. **Test transactions** — Verify isolation levels work correctly for concurrent operations
7. **Set up migrations** — Initialize Alembic, create initial migration, apply it
8. **Backup strategy** — Create a `pg_dump` backup, test restore to a new database
9. **Monitor** — Query `pg_stat_user_tables` and `pg_stat_user_indexes` for table/index usage stats

```sql
-- Production monitoring queries
SELECT schemaname, relname, seq_scan, idx_scan, n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables ORDER BY seq_scan DESC;

SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes ORDER BY idx_scan DESC;

SELECT datname, numbackends, xact_commit, xact_rollback, blks_read, blks_hit,
       round(blks_hit::numeric / (blks_hit + blks_read + 1), 3) AS cache_hit_ratio
FROM pg_stat_database WHERE datname = 'labdb';
```

---

## Key Takeaways

1. **Design schemas with constraints** — Let the database enforce data integrity, not just your application.
2. **Index strategically** — `EXPLAIN ANALYZE` is your best friend for finding missing indexes.
3. **Understand transactions** — Use the lowest isolation level that meets your requirements.
4. **Version your schema** — Never manually `ALTER TABLE` in production. Use Alembic or similar.
5. **Always use volumes** — Container databases without volumes lose all data on restart.
6. **Monitor continuously** — `pg_stat_activity`, `pg_stat_user_tables`, and cache hit ratio are essential.

---
*Next: [Section 15 — Elasticsearch Practice](15-elasticsearch-practice.md)*
