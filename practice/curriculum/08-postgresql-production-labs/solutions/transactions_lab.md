# Transactions Lab — Reference Walkthrough

## Part 1: Isolation Levels

### READ COMMITTED (Default)

- Each statement within a transaction sees the latest committed data
- A second `SELECT` in the same transaction CAN see changes committed by other transactions between the two reads
- This is called a **non-repeatable read**

### REPEATABLE READ

- The transaction sees a snapshot of data as of the transaction's start
- Subsequent reads return the same data even if other transactions commit changes
- Attempting to UPDATE a row modified by another concurrent transaction raises a serialization error:
  ```
  ERROR: could not serialize access due to concurrent update
  ```

### SERIALIZABLE

- Strictest level — transactions execute as if they ran one at a time
- May raise serialization errors more frequently
- Safest for correctness, worst for concurrency

## Part 2: Lock Contention

### What happens

1. Session A acquires a **RowExclusiveLock** on `accounts` row id=1
2. Session B tries to UPDATE the same row and **blocks** (waits)
3. When Session A commits, the lock is released
4. Session B proceeds with its update

### How to observe locks

```sql
-- Run in a third session while Session B is blocked:
SELECT pid, mode, relation::regclass, granted
FROM pg_locks
WHERE relation = 'accounts'::regclass;
```

Expected output shows two locks: one granted (Session A), one waiting (Session B).

### Lock wait timeout

Set a timeout to avoid indefinite waits:

```sql
SET lock_timeout = '5s';
```

## Part 3: Deadlock

### What happens

1. Session A locks row id=1
2. Session B locks row id=2
3. Session A tries to lock row id=2 → waits for Session B
4. Session B tries to lock row id=1 → waits for Session A
5. **Deadlock detected** — Postgres aborts one transaction (typically the one that caused the cycle)

### Error message

```
ERROR:  deadlock detected
DETAIL:  Process 123 waits for ShareLock on transaction 456; blocked by process 789.
Process 789 waits for ShareLock on transaction 012; blocked by process 123.
HINT:  See server log for query details.
```

### Prevention strategies

1. **Consistent lock ordering** — always lock rows in the same order (e.g., by id ASC)
2. **Short transactions** — minimize the time locks are held
3. **Lock timeout** — `SET lock_timeout = '5s'` to fail fast
4. **Advisory locks** — use `pg_advisory_lock()` for application-level coordination
5. **SELECT ... FOR UPDATE NOWAIT** — fail immediately if lock not available

## Summary Table

| Level | Dirty Read | Non-repeatable Read | Phantom Read | Performance |
|-------|-----------|-------------------|-------------|-------------|
| READ UNCOMMITTED | Yes* | Yes | Yes | Best |
| READ COMMITTED | No | Yes | Yes | Good |
| REPEATABLE READ | No | No | No** | Moderate |
| SERIALIZABLE | No | No | No | Worst |

*PostgreSQL treats READ UNCOMMITTED as READ COMMITTED
**PostgreSQL's REPEATABLE READ also prevents phantom reads (unlike the SQL standard minimum)
