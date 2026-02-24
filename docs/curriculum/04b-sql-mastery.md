# SECTION 4b — SQL MASTERY

---

## PART A — CONCEPT EXPLANATION

### Why Dedicated SQL Practice Matters

Section 4 introduced basic CRUD. Section 8 covers PostgreSQL production ops. This section fills the gap — you need **fluent SQL** to:
- **Write efficient queries** — JOINs, subqueries, and window functions are everyday tools
- **Debug production issues** — "Why is this report wrong?" usually means a bad JOIN or missing filter
- **Understand ORMs** — SQLAlchemy, Django ORM, and Prisma all generate SQL; reading that SQL is essential
- **Pass interviews** — SQL is one of the most commonly tested skills for backend/data/infra roles

### Setup: Practice Database

All exercises use PostgreSQL via Docker. Start the database:

```bash
cd practice/curriculum/04-database
docker compose up -d
docker compose exec postgres psql -U labuser -d labdb
```

Or use the existing setup from Section 08 labs.

---

### 1. SELECT Fundamentals

```sql
-- Basic SELECT
SELECT title, status, priority FROM tasks;

-- Filtering with WHERE
SELECT * FROM tasks WHERE status = 'open' AND priority >= 3;

-- Comparison operators: =, !=, <>, <, >, <=, >=
-- Logical operators: AND, OR, NOT

-- BETWEEN (inclusive range)
SELECT * FROM tasks WHERE priority BETWEEN 2 AND 4;

-- IN (set membership)
SELECT * FROM tasks WHERE status IN ('open', 'in_progress');

-- LIKE (pattern matching)
SELECT * FROM users WHERE email LIKE '%@gmail.com';
-- % = any characters, _ = single character

-- IS NULL / IS NOT NULL
SELECT * FROM tasks WHERE assigned_to IS NULL;

-- DISTINCT (unique values)
SELECT DISTINCT status FROM tasks;

-- ORDER BY
SELECT * FROM tasks ORDER BY priority DESC, created_at ASC;

-- LIMIT and OFFSET (pagination)
SELECT * FROM tasks ORDER BY created_at DESC LIMIT 10 OFFSET 20;
```

### 2. Aggregate Functions

Aggregates compute a single value from a set of rows:

```sql
-- COUNT — number of rows
SELECT COUNT(*) FROM tasks;
SELECT COUNT(DISTINCT status) FROM tasks;

-- SUM — total
SELECT SUM(priority) FROM tasks WHERE status = 'open';

-- AVG — average
SELECT AVG(priority) FROM tasks;

-- MIN / MAX
SELECT MIN(created_at), MAX(created_at) FROM tasks;

-- Combining aggregates
SELECT
    COUNT(*) AS total_tasks,
    COUNT(*) FILTER (WHERE status = 'open') AS open_tasks,
    AVG(priority) AS avg_priority,
    MAX(priority) AS max_priority
FROM tasks;
```

### 3. GROUP BY and HAVING

`GROUP BY` creates groups; aggregates compute per group. `HAVING` filters groups (like `WHERE` for groups).

```sql
-- Tasks per status
SELECT status, COUNT(*) AS task_count
FROM tasks
GROUP BY status;

-- Tasks per user, only users with 3+ tasks
SELECT assigned_to, COUNT(*) AS task_count
FROM tasks
GROUP BY assigned_to
HAVING COUNT(*) >= 3;

-- Multiple grouping columns
SELECT status, priority, COUNT(*)
FROM tasks
GROUP BY status, priority
ORDER BY status, priority;
```

**Common mistake:** Using a non-aggregated column without it being in GROUP BY.
```sql
-- WRONG: title is not in GROUP BY or an aggregate
SELECT status, title, COUNT(*) FROM tasks GROUP BY status;

-- RIGHT: aggregate or include in GROUP BY
SELECT status, COUNT(*), ARRAY_AGG(title) FROM tasks GROUP BY status;
```

### 4. JOIN Types

JOINs combine rows from two or more tables based on a related column.

```
users                    tasks
┌────┬──────────┐       ┌────┬───────────┬─────────────┐
│ id │ username │       │ id │ title     │ assigned_to │
├────┼──────────┤       ├────┼───────────┼─────────────┤
│ 1  │ alice    │       │ 1  │ Fix bug   │ 1           │
│ 2  │ bob      │       │ 2  │ Add test  │ 1           │
│ 3  │ charlie  │       │ 3  │ Deploy    │ 2           │
└────┴──────────┘       │ 4  │ Review    │ NULL        │
                        └────┴───────────┴─────────────┘
```

**INNER JOIN** — Only matching rows from both tables:
```sql
SELECT u.username, t.title
FROM users u
INNER JOIN tasks t ON u.id = t.assigned_to;
-- Returns: alice/Fix bug, alice/Add test, bob/Deploy
-- Excludes: charlie (no tasks), Review (no assignee)
```

**LEFT JOIN** — All rows from left table, matching from right (NULL if no match):
```sql
SELECT u.username, t.title
FROM users u
LEFT JOIN tasks t ON u.id = t.assigned_to;
-- Returns: alice/Fix bug, alice/Add test, bob/Deploy, charlie/NULL
```

**RIGHT JOIN** — All rows from right table, matching from left:
```sql
SELECT u.username, t.title
FROM users u
RIGHT JOIN tasks t ON u.id = t.assigned_to;
-- Returns: alice/Fix bug, alice/Add test, bob/Deploy, NULL/Review
```

**FULL OUTER JOIN** — All rows from both tables:
```sql
SELECT u.username, t.title
FROM users u
FULL OUTER JOIN tasks t ON u.id = t.assigned_to;
-- Returns: all 5 rows (charlie/NULL and NULL/Review included)
```

**CROSS JOIN** — Cartesian product (every combination):
```sql
SELECT u.username, t.title
FROM users u
CROSS JOIN tasks t;
-- Returns: 3 users × 4 tasks = 12 rows
```

**Self JOIN** — Table joined to itself (e.g., manager/employee):
```sql
SELECT e.username AS employee, m.username AS manager
FROM users e
LEFT JOIN users m ON e.manager_id = m.id;
```

**Multi-table JOINs:**
```sql
SELECT
    t.title,
    u.username AS assignee,
    p.name AS project
FROM tasks t
JOIN users u ON t.assigned_to = u.id
JOIN projects p ON t.project_id = p.id
WHERE t.status = 'open';
```

### 5. Subqueries

A subquery is a query nested inside another query.

**Scalar subquery** — Returns a single value:
```sql
SELECT title, priority
FROM tasks
WHERE priority > (SELECT AVG(priority) FROM tasks);
```

**IN subquery** — Returns a set:
```sql
SELECT username FROM users
WHERE id IN (SELECT DISTINCT assigned_to FROM tasks WHERE status = 'open');
```

**EXISTS subquery** — Returns true if any row exists:
```sql
-- Users who have at least one task
SELECT username FROM users u
WHERE EXISTS (SELECT 1 FROM tasks t WHERE t.assigned_to = u.id);

-- Users who have NO tasks
SELECT username FROM users u
WHERE NOT EXISTS (SELECT 1 FROM tasks t WHERE t.assigned_to = u.id);
```

**Correlated subquery** — References the outer query (runs once per outer row):
```sql
-- Tasks where priority is above their project's average
SELECT t.title, t.priority
FROM tasks t
WHERE t.priority > (
    SELECT AVG(t2.priority)
    FROM tasks t2
    WHERE t2.project_id = t.project_id
);
```

**FROM subquery (derived table):**
```sql
SELECT project_name, task_count
FROM (
    SELECT p.name AS project_name, COUNT(*) AS task_count
    FROM projects p
    JOIN tasks t ON p.id = t.project_id
    GROUP BY p.name
) AS project_stats
WHERE task_count > 5;
```

### 6. Common Table Expressions (CTEs)

CTEs make complex queries readable by naming intermediate results with `WITH`:

```sql
-- Named intermediate results
WITH open_tasks AS (
    SELECT * FROM tasks WHERE status = 'open'
),
user_task_counts AS (
    SELECT assigned_to, COUNT(*) AS task_count
    FROM open_tasks
    GROUP BY assigned_to
)
SELECT u.username, utc.task_count
FROM user_task_counts utc
JOIN users u ON utc.assigned_to = u.id
ORDER BY utc.task_count DESC;
```

**Recursive CTE** — For hierarchical data (org charts, categories, threaded comments):
```sql
-- Employee hierarchy
WITH RECURSIVE org_chart AS (
    -- Base case: top-level (no manager)
    SELECT id, username, manager_id, 1 AS depth
    FROM users
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: find direct reports
    SELECT u.id, u.username, u.manager_id, oc.depth + 1
    FROM users u
    JOIN org_chart oc ON u.manager_id = oc.id
)
SELECT depth, username FROM org_chart ORDER BY depth, username;
```

### 7. Window Functions

Window functions compute values across a set of rows **without collapsing them** (unlike GROUP BY):

```sql
-- ROW_NUMBER — sequential numbering within a partition
SELECT
    title,
    status,
    ROW_NUMBER() OVER (PARTITION BY status ORDER BY created_at) AS row_num
FROM tasks;

-- RANK — like ROW_NUMBER but ties get the same rank (gaps after)
-- DENSE_RANK — like RANK but no gaps
SELECT
    title,
    priority,
    RANK() OVER (ORDER BY priority DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY priority DESC) AS dense_rank
FROM tasks;

-- LAG / LEAD — access previous/next row's value
SELECT
    title,
    created_at,
    LAG(created_at) OVER (ORDER BY created_at) AS prev_created,
    created_at - LAG(created_at) OVER (ORDER BY created_at) AS gap
FROM tasks;

-- Running totals with SUM OVER
SELECT
    created_at::date AS day,
    COUNT(*) AS daily_count,
    SUM(COUNT(*)) OVER (ORDER BY created_at::date) AS running_total
FROM tasks
GROUP BY created_at::date
ORDER BY day;

-- FIRST_VALUE / LAST_VALUE
SELECT
    title,
    status,
    FIRST_VALUE(title) OVER (PARTITION BY status ORDER BY priority DESC) AS highest_priority_task
FROM tasks;

-- NTILE — divide rows into N buckets
SELECT
    title,
    priority,
    NTILE(4) OVER (ORDER BY priority DESC) AS quartile
FROM tasks;
```

**Window frame specification:**
```sql
-- Moving average of last 7 days
SELECT
    day,
    daily_count,
    AVG(daily_count) OVER (
        ORDER BY day
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7d
FROM daily_stats;
```

### 8. Set Operations

Combine results from multiple queries:

```sql
-- UNION — all unique rows from both queries
SELECT username FROM active_users
UNION
SELECT username FROM admin_users;

-- UNION ALL — all rows (including duplicates, faster)
SELECT username FROM active_users
UNION ALL
SELECT username FROM admin_users;

-- INTERSECT — rows in both queries
SELECT username FROM active_users
INTERSECT
SELECT username FROM admin_users;

-- EXCEPT — rows in first but not second
SELECT username FROM active_users
EXCEPT
SELECT username FROM admin_users;
```

### 9. CASE Expressions

Conditional logic within SQL:

```sql
-- Simple CASE
SELECT
    title,
    priority,
    CASE priority
        WHEN 5 THEN 'Critical'
        WHEN 4 THEN 'High'
        WHEN 3 THEN 'Medium'
        ELSE 'Low'
    END AS priority_label
FROM tasks;

-- Searched CASE (with conditions)
SELECT
    title,
    CASE
        WHEN status = 'closed' AND updated_at > NOW() - INTERVAL '1 day' THEN 'Recently closed'
        WHEN status = 'open' AND priority >= 4 THEN 'Urgent'
        WHEN status = 'open' THEN 'Normal'
        ELSE 'Other'
    END AS category
FROM tasks;

-- CASE in aggregation (pivot-like)
SELECT
    project_id,
    COUNT(*) FILTER (WHERE status = 'open') AS open_count,
    COUNT(*) FILTER (WHERE status = 'in_progress') AS in_progress_count,
    COUNT(*) FILTER (WHERE status = 'closed') AS closed_count
FROM tasks
GROUP BY project_id;
```

### 10. Essential Functions

**String functions:**
```sql
SELECT
    UPPER(username),                    -- ALICE
    LOWER(email),                       -- alice@test.com
    LENGTH(username),                   -- 5
    CONCAT(username, ' <', email, '>'), -- alice <alice@test.com>
    SUBSTRING(email FROM 1 FOR 5),      -- alice
    REPLACE(email, '@', ' [at] '),      -- alice [at] test.com
    TRIM('  hello  '),                  -- hello
    LEFT(title, 20),                    -- First 20 characters
    SPLIT_PART(email, '@', 2)           -- test.com
FROM users;
```

**Date/Time functions:**
```sql
SELECT
    NOW(),                                         -- Current timestamp
    CURRENT_DATE,                                  -- Today's date
    DATE_TRUNC('month', created_at),               -- First of the month
    EXTRACT(YEAR FROM created_at),                 -- Year as number
    AGE(NOW(), created_at),                        -- Interval since creation
    created_at + INTERVAL '30 days',               -- 30 days later
    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS')  -- Formatted string
FROM tasks;
```

**Conditional functions:**
```sql
SELECT
    COALESCE(assigned_to, 0) AS assignee,      -- First non-NULL value
    NULLIF(status, 'unknown') AS status,       -- NULL if equal
    GREATEST(priority, 3) AS min_priority_3,   -- Max of values
    LEAST(priority, 3) AS max_priority_3       -- Min of values
FROM tasks;
```

### 11. Views

**Regular view** — Saved query (re-executes each time):
```sql
CREATE VIEW open_task_summary AS
SELECT
    p.name AS project,
    u.username AS assignee,
    COUNT(*) AS open_tasks,
    MAX(t.priority) AS highest_priority
FROM tasks t
JOIN projects p ON t.project_id = p.id
LEFT JOIN users u ON t.assigned_to = u.id
WHERE t.status = 'open'
GROUP BY p.name, u.username;

-- Use like a table
SELECT * FROM open_task_summary WHERE open_tasks > 5;
```

**Materialized view** — Cached result (must refresh manually):
```sql
CREATE MATERIALIZED VIEW daily_task_stats AS
SELECT
    created_at::date AS day,
    COUNT(*) AS tasks_created,
    COUNT(*) FILTER (WHERE status = 'closed') AS tasks_closed
FROM tasks
GROUP BY created_at::date;

-- Refresh when data changes
REFRESH MATERIALIZED VIEW daily_task_stats;

-- Refresh without locking reads
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_task_stats;
```

### Common Beginner Misunderstandings

1. **"LEFT JOIN and JOIN are the same"** — `JOIN` (inner) drops rows with no match. `LEFT JOIN` keeps all left-table rows with NULLs for missing matches. This distinction matters enormously.
2. **"Subqueries are always slow"** — PostgreSQL's optimizer often rewrites subqueries into JOINs. Use whichever is more readable; profile if performance matters.
3. **"Window functions collapse rows like GROUP BY"** — No. Window functions add computed columns while preserving every row. That's what makes them powerful.
4. **"CTEs are just for readability"** — CTEs also enable recursion, and in PostgreSQL 12+ they can be inlined by the optimizer.
5. **"UNION removes duplicates"** — Yes, but it's slower. Use `UNION ALL` when you know there are no duplicates or duplicates are acceptable.

---

## PART B — BEGINNER PRACTICE

### Exercise B.1 — Setup: Create and Populate Tables

Create the practice schema and insert sample data. This is the foundation for all exercises.

```bash
cd practice/curriculum/04-database
docker compose exec -T postgres psql -U labuser -d labdb < B_sql_fundamentals.sql
```

**Practice file:** `practice/curriculum/04-database/B_sql_fundamentals.sql`

### Exercise B.2 — Basic SELECT and Filtering

Write queries to answer:
1. All employees in the Engineering department
2. Products with price between $10 and $50
3. Customers whose email contains "gmail"
4. Orders placed in the last 30 days
5. Products that have no description (NULL)

### Exercise B.3 — Sorting and Pagination

1. All products sorted by price descending
2. The 10 most recent orders
3. Top 5 highest-paid employees
4. Products page 3 (items 21-30) sorted by name

### Exercise B.4 — Aggregate Functions

1. Total number of orders
2. Average order amount
3. Most expensive product
4. Earliest and latest order dates
5. Number of distinct departments

### Exercise B.5 — GROUP BY and HAVING

1. Number of employees per department
2. Total sales per product
3. Average order amount per customer
4. Departments with more than 5 employees
5. Products ordered more than 10 times

### Exercise B.6 — Simple JOINs

1. All orders with customer name (INNER JOIN)
2. All customers with their orders — include customers with no orders (LEFT JOIN)
3. Order details with product name and price
4. Employees with their department name

---

## PART C — INTERMEDIATE PRACTICE

### Exercise C.1 — Multi-table JOINs

1. Full order report: order ID, customer name, product name, quantity, line total
2. Employee directory: name, department, manager name (self-join)
3. Products never ordered (LEFT JOIN + IS NULL or NOT EXISTS)
4. Customers who ordered every product (division query)

### Exercise C.2 — Subqueries

1. Products with above-average price
2. Customers who placed orders in January (IN subquery)
3. The most recent order for each customer (correlated subquery)
4. Departments where all employees earn above $50,000 (NOT EXISTS)
5. Second highest salary in each department

### Exercise C.3 — CTEs

1. Rewrite a complex JOIN + aggregation as a CTE pipeline
2. Monthly revenue report using a CTE for date ranges
3. Recursive CTE: org chart showing employee → manager chain
4. Recursive CTE: category tree with depth labels

### Exercise C.4 — Window Functions

1. Rank employees by salary within each department (RANK, DENSE_RANK)
2. Running total of daily sales (SUM OVER)
3. Difference between each order and the previous order (LAG)
4. Top 3 products by revenue in each category (ROW_NUMBER + filter)
5. Moving average of order amounts over 7-day window

### Exercise C.5 — CASE and Conditional Logic

1. Categorize products as 'Budget', 'Mid-range', 'Premium' by price
2. Pivot: count orders by status (open, shipped, delivered) per month
3. Calculate bonus: 10% for sales > $100K, 5% for > $50K, 0% otherwise
4. Flag overdue tasks (status = open AND created > 7 days ago)

### Exercise C.6 — Set Operations

1. UNION: Combine active and archived customer lists
2. INTERSECT: Customers who ordered in both Q1 and Q2
3. EXCEPT: Products in catalog but never ordered
4. UNION ALL with source labels: combine two audit tables

---

## PART D — ADVANCED DEBUG LAB

### Exercise D.1 — Debug: Wrong JOIN Produces Duplicates

**Symptom:** Report shows 500 orders but database has 200.

**Cause:** Missing JOIN condition creates a partial cartesian product.

**Task:**
1. Run the buggy query, observe the inflated row count
2. Identify the missing or incorrect ON clause
3. Fix the query, verify row count matches expectations

```sql
-- BUGGY: Missing join condition
SELECT c.name, o.id, p.name
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON TRUE  -- BUG: should be p.id = oi.product_id
;
```

### Exercise D.2 — Debug: GROUP BY Hides Data

**Symptom:** Sum of department salaries doesn't match total payroll.

**Cause:** Employees with NULL department are excluded from grouped results.

**Task:**
1. Run `SELECT department, SUM(salary) FROM employees GROUP BY department`
2. Compare with `SELECT SUM(salary) FROM employees`
3. Fix with `COALESCE(department, 'Unassigned')`

### Exercise D.3 — Debug: Subquery Returns Wrong Results

**Symptom:** "Find customers who haven't ordered" returns 0 rows, but you know some exist.

**Cause:** Using `NOT IN` with a subquery that returns NULLs.

```sql
-- BUGGY: If any customer_id in orders is NULL, NOT IN returns empty
SELECT * FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);

-- FIX 1: Filter NULLs
WHERE id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);

-- FIX 2: Use NOT EXISTS (preferred)
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = customers.id);
```

### Exercise D.4 — Debug: Window Function Boundary Error

**Symptom:** Moving average includes future data.

**Task:**
1. Identify incorrect window frame (`ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING`)
2. Fix to only look backward (`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`)
3. Add `ORDER BY` within the window (missing ORDER BY gives wrong results)

### Exercise D.5 — Debug: Slow Query — Missing Index on JOIN Column

**Symptom:** Dashboard query takes 12 seconds on 100K rows.

**Task:**
1. Run `EXPLAIN ANALYZE` on the slow query
2. Identify `Seq Scan` on foreign key column used in JOIN
3. Add index: `CREATE INDEX idx_orders_customer_id ON orders(customer_id);`
4. Re-run `EXPLAIN ANALYZE`, verify `Index Scan` and sub-second execution

### Exercise D.6 — Debug: Incorrect OUTER JOIN Filter

**Symptom:** LEFT JOIN behaves like INNER JOIN — unmatched rows disappear.

**Cause:** Filtering the right table in WHERE instead of in the ON clause.

```sql
-- BUGGY: WHERE filter eliminates NULL rows from LEFT JOIN
SELECT c.name, o.total
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'completed';  -- This removes customers with no orders

-- FIX: Move filter to ON clause
SELECT c.name, o.total
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id AND o.status = 'completed';
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Build a Reporting Database

You are building the analytics layer for an e-commerce platform:

1. **Design schema** — Create tables: `customers`, `products`, `categories`, `orders`, `order_items`, `employees`, `departments`
2. **Seed data** — Insert 10K+ rows of realistic data with `generate_series` and `random()`
3. **Write reports:**
   - Monthly revenue with month-over-month growth (window functions)
   - Top 10 customers by lifetime value (CTEs + aggregation)
   - Product category performance with rankings (RANK, window functions)
   - Employee performance by department (self-join for managers + aggregation)
   - Inventory alert: products with low stock that sell frequently (subquery + HAVING)
4. **Create views** — Materialize the top 3 reports as views
5. **Optimize** — Run `EXPLAIN ANALYZE` on each report, add indexes to bring all under 100ms
6. **Document** — Write a `queries.md` explaining each report query

**Practice files:** `practice/curriculum/04-database/E_sql_production.sql`

---

## Key Takeaways

1. **JOINs are the backbone of relational queries** — Master all types. Know when LEFT JOIN vs INNER JOIN changes your result set.
2. **Window functions preserve rows** — Unlike GROUP BY, they add computed columns without collapsing data. Essential for rankings, running totals, and gap analysis.
3. **CTEs > nested subqueries** — Named intermediate results are easier to read, debug, and maintain.
4. **NULL is not a value — it's the absence of one** — `NULL = NULL` is not `TRUE`. Use `IS NULL`, `COALESCE`, and `NOT EXISTS` instead of `NOT IN`.
5. **Always EXPLAIN ANALYZE** — Reading query plans is a production skill. Do it before deploying any query that touches more than 1000 rows.
6. **Write readable SQL** — Uppercase keywords, alias tables, indent subqueries. You'll read your SQL far more than you write it.

---
*Next: [Section 5 — REST API Design](05-rest-api-design.md)*
