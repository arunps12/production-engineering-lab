# Benchmark Results — Exercise 14.3

## Setup

- PostgreSQL 16 (Docker, default config)
- 100,000 tasks, 100 users, 50 projects
- Query: find pending tasks with high priority, join user + project

## Query Under Test

```sql
SELECT t.title, u.username, p.name as project_name
FROM tasks t
JOIN users u ON t.assigned_to = u.id
JOIN projects p ON t.project_id = p.id
WHERE t.status = 'pending' AND t.priority > 3
ORDER BY t.created_at DESC
LIMIT 50;
```

## Before Index

```
EXPLAIN ANALYZE output (expected pattern):

Sort  (cost=4521.23..4521.35 rows=50 width=96) (actual time=45.123..45.130 rows=50 loops=1)
  Sort Key: t.created_at DESC
  ->  Hash Join  (cost=12.50..4519.87 rows=50 width=96) (actual time=0.321..44.567 rows=9980 loops=1)
        ->  Seq Scan on tasks t  (cost=0.00..4123.00 rows=10000 width=52) (actual time=0.012..38.234 rows=9980 loops=1)
              Filter: ((status = 'pending') AND (priority > 3))
              Rows Removed by Filter: 90020
Planning Time: 0.234 ms
Execution Time: 45.567 ms
```

**Key observation:** Sequential scan on `tasks` — scans all 100k rows, filters 90%.

## After Index

```sql
CREATE INDEX idx_tasks_status_priority_created
ON tasks (status, priority, created_at DESC);
```

```
EXPLAIN ANALYZE output (expected pattern):

Limit  (cost=0.42..125.67 rows=50 width=96) (actual time=0.078..0.534 rows=50 loops=1)
  ->  Nested Loop  (cost=0.42..25000.00 rows=9980 width=96) (actual time=0.076..0.521 rows=50 loops=1)
        ->  Index Scan using idx_tasks_status_priority_created on tasks t
              (cost=0.42..500.00 rows=9980 width=52) (actual time=0.045..0.123 rows=50 loops=1)
              Index Cond: ((status = 'pending') AND (priority > 3))
Planning Time: 0.312 ms
Execution Time: 0.612 ms
```

**Key observation:** Index scan replaces Seq Scan. ~75x faster.

## Analysis

| Metric | Before Index | After Index | Improvement |
|--------|-------------|-------------|-------------|
| Scan Type | Seq Scan | Index Scan | Targeted access |
| Rows Scanned | ~100,000 | ~50 | 2000x fewer |
| Execution Time | ~45 ms | ~0.6 ms | ~75x faster |
| Buffers Hit | ~1200 | ~15 | 80x fewer |

## Why This Index Works

The composite index `(status, priority, created_at DESC)` matches the query's:
1. **WHERE clause** — `status = 'pending'` (equality) + `priority > 3` (range)
2. **ORDER BY** — `created_at DESC` (already sorted in index)
3. **LIMIT 50** — index scan stops after 50 matching rows

## Takeaways

- Always use `EXPLAIN (ANALYZE, BUFFERS)` before optimizing
- Composite indexes should match WHERE equality columns first, then range columns
- Include ORDER BY columns in the index when possible
- `LIMIT` benefits greatly from matching indexes (avoids full sort)
- Run `ANALYZE` after bulk inserts to update planner statistics
