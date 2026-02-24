-- =============================================================================
-- Section 4b — SQL Mastery: Advanced Debug + Production (D.1–D.6, E.1)
-- Guide: docs/curriculum/04b-sql-mastery.md
--
-- Prerequisites: Run B_sql_fundamentals.sql first to create tables.
-- Run: docker compose exec -T postgres psql -U labuser -d labdb < D_sql_advanced.sql
-- =============================================================================


-- ─────────────────────────────────────────────────────────────────────────────
-- Bulk Data Generation (needed for performance exercises)
-- ─────────────────────────────────────────────────────────────────────────────

-- Generate 50K products for performance testing
INSERT INTO products (name, description, price, category_id, stock, created_at)
SELECT
    'Product ' || i,
    CASE WHEN random() < 0.1 THEN NULL ELSE 'Description for product ' || i END,
    ROUND((random() * 2000 + 1)::numeric, 2),
    (ARRAY[1,2,3,4,5,6,7,8,9])[floor(random() * 9 + 1)::int],
    floor(random() * 1000)::int,
    NOW() - (random() * 365)::int * INTERVAL '1 day'
FROM generate_series(100, 50099) AS i;

-- Generate 10K customers for performance testing
INSERT INTO customers (name, email, city, created_at)
SELECT
    'Customer ' || i,
    'customer' || i || '@test.com',
    (ARRAY['New York','San Francisco','Austin','Seattle','Boston',
           'Portland','Chicago','Denver','Miami','Atlanta'])[floor(random() * 10 + 1)::int],
    NOW() - (random() * 730)::int * INTERVAL '1 day'
FROM generate_series(100, 10099) AS i;

-- Generate 100K orders
INSERT INTO orders (customer_id, status, total, created_at)
SELECT
    floor(random() * 10000 + 100)::int,
    (ARRAY['pending','shipped','delivered','delivered','delivered','cancelled'])
        [floor(random() * 6 + 1)::int],
    ROUND((random() * 5000 + 5)::numeric, 2),
    NOW() - (random() * 365)::int * INTERVAL '1 day'
        + (random() * 86400)::int * INTERVAL '1 second'
FROM generate_series(1, 100000);

-- Generate 200K order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT
    floor(random() * 100000 + 12)::int,
    floor(random() * 50000 + 100)::int,
    floor(random() * 5 + 1)::int,
    ROUND((random() * 500 + 1)::numeric, 2)
FROM generate_series(1, 200000);

-- Analyze tables for accurate query planning
ANALYZE products;
ANALYZE customers;
ANALYZE orders;
ANALYZE order_items;

SELECT '=== BULK DATA LOADED ===' AS info;
SELECT 'products' AS tbl, COUNT(*) AS rows FROM products
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
ORDER BY tbl;


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise D.1 — Debug: Wrong JOIN Produces Duplicates
-- ─────────────────────────────────────────────────────────────────────────────
-- SYMPTOM: Expected ~15 order items but query returns thousands of rows.
-- TASK: Find and fix the bug.

-- BUGGY QUERY — Run this and observe the inflated row count:
-- SELECT c.name AS customer, o.id AS order_id, p.name AS product
-- FROM customers c
-- JOIN orders o ON c.id = o.customer_id
-- JOIN order_items oi ON o.id = oi.order_id
-- JOIN products p ON TRUE     -- BUG! Should be: p.id = oi.product_id
-- LIMIT 50;

-- TODO: Fix the JOIN condition and verify the count matches order_items
-- SELECT COUNT(*) FROM order_items;  -- Expected count


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise D.2 — Debug: GROUP BY Hides NULL Data
-- ─────────────────────────────────────────────────────────────────────────────
-- SYMPTOM: Sum of department salaries doesn't match total payroll.

-- Run these two queries and compare:
-- SELECT SUM(salary) AS total_payroll FROM employees;
-- SELECT d.name, SUM(e.salary) AS dept_payroll
-- FROM employees e
-- JOIN departments d ON e.department_id = d.id   -- INNER JOIN misses NULL dept
-- GROUP BY d.name;

-- TODO: Fix so the totals match
-- Hint: Use LEFT JOIN and COALESCE(d.name, 'Unassigned')


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise D.3 — Debug: NOT IN Fails with NULLs
-- ─────────────────────────────────────────────────────────────────────────────
-- SYMPTOM: "Find customers who haven't ordered" returns 0 rows
-- but InactiveInc (id=7) definitely has no orders.

-- BUGGY QUERY:
-- SELECT name FROM customers
-- WHERE id NOT IN (SELECT customer_id FROM orders);
-- This returns empty if ANY customer_id in orders is NULL!

-- FIX 1: Filter NULLs in subquery
-- WHERE id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);

-- FIX 2: Use NOT EXISTS (always correct, preferred)
-- SELECT name FROM customers c
-- WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- TODO: Run both buggy and fixed versions, verify results.


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise D.4 — Debug: LEFT JOIN Acts Like INNER JOIN
-- ─────────────────────────────────────────────────────────────────────────────
-- SYMPTOM: LEFT JOIN should show all customers, but unmatched ones disappear.

-- BUGGY QUERY:
-- SELECT c.name, o.total, o.status
-- FROM customers c
-- LEFT JOIN orders o ON c.id = o.customer_id
-- WHERE o.status = 'delivered';    -- BUG: filters out NULLs from LEFT JOIN

-- TODO: Fix by moving the filter to the ON clause:
-- LEFT JOIN orders o ON c.id = o.customer_id AND o.status = 'delivered'


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise D.5 — Debug: Slow Query — Missing Index
-- ─────────────────────────────────────────────────────────────────────────────
-- SYMPTOM: Query takes seconds on 100K rows.

-- TASK:
-- 1. Run EXPLAIN ANALYZE on this query:
-- EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
-- SELECT c.name, SUM(o.total) AS lifetime_value
-- FROM customers c
-- JOIN orders o ON c.id = o.customer_id
-- WHERE o.created_at >= '2025-01-01'
--   AND o.status = 'delivered'
-- GROUP BY c.name
-- ORDER BY lifetime_value DESC
-- LIMIT 10;

-- 2. Look for Seq Scan on orders table
-- 3. Add appropriate indexes:
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
-- CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- 4. Run EXPLAIN ANALYZE again, compare execution times


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise D.6 — Debug: Window Function Misuse
-- ─────────────────────────────────────────────────────────────────────────────
-- SYMPTOM: "Running average" includes future data.

-- BUGGY QUERY — uses default frame (RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
-- but with no ORDER BY it uses the whole partition):
-- SELECT
--     created_at::date AS day,
--     total,
--     AVG(total) OVER () AS avg_total  -- BUG: averages ALL rows, not running
-- FROM orders
-- LIMIT 20;

-- TODO: Fix with proper window specification:
-- AVG(total) OVER (ORDER BY created_at ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
-- AS moving_avg_7d


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise E.1 — Production Simulation: Analytics Dashboard
-- ─────────────────────────────────────────────────────────────────────────────

-- Build these production-grade reports. Each should run under 100ms on the
-- bulk data. Use EXPLAIN ANALYZE to verify. Add indexes as needed.

-- REPORT 1: Monthly Revenue with Month-over-Month Growth
-- TODO: Write a CTE with monthly revenue, then use LAG to compute growth %
-- WITH monthly_revenue AS (
--     SELECT DATE_TRUNC('month', created_at) AS month,
--            SUM(total) AS revenue
--     FROM orders
--     WHERE status != 'cancelled'
--     GROUP BY DATE_TRUNC('month', created_at)
-- )
-- SELECT
--     TO_CHAR(month, 'YYYY-MM') AS month,
--     revenue,
--     LAG(revenue) OVER (ORDER BY month) AS prev_month,
--     ROUND(
--         (revenue - LAG(revenue) OVER (ORDER BY month))
--         / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100
--     , 1) AS growth_pct
-- FROM monthly_revenue
-- ORDER BY month;


-- REPORT 2: Top 10 Customers by Lifetime Value
-- TODO: SUM(total) grouped by customer, exclude cancelled
-- WITH customer_ltv AS (...)
-- SELECT ... ORDER BY lifetime_value DESC LIMIT 10;


-- REPORT 3: Product Category Performance
-- TODO: Revenue per category with rank
-- WITH category_revenue AS (
--     SELECT c.name AS category,
--            SUM(oi.quantity * oi.unit_price) AS revenue,
--            COUNT(DISTINCT oi.order_id) AS order_count
--     FROM order_items oi
--     JOIN products p ON oi.product_id = p.id
--     JOIN categories c ON p.category_id = c.id
--     GROUP BY c.name
-- )
-- SELECT category, revenue, order_count,
--        RANK() OVER (ORDER BY revenue DESC) AS rank
-- FROM category_revenue;


-- REPORT 4: Low Stock Alert — Products that sell frequently but have low stock
-- TODO: Products with stock < 50 AND total quantity sold > 20
-- SELECT p.name, p.stock,
--        COALESCE(SUM(oi.quantity), 0) AS total_sold
-- FROM products p
-- LEFT JOIN order_items oi ON p.id = oi.product_id
-- GROUP BY p.id, p.name, p.stock
-- HAVING p.stock < 50 AND COALESCE(SUM(oi.quantity), 0) > 20
-- ORDER BY total_sold DESC;


-- REPORT 5: Create a materialized view for the monthly revenue report
-- TODO:
-- CREATE MATERIALIZED VIEW IF NOT EXISTS mv_monthly_revenue AS
-- SELECT ... (copy from REPORT 1)
-- ;
-- REFRESH MATERIALIZED VIEW mv_monthly_revenue;


-- ─────────────────────────────────────────────────────────────────────────────
-- Optimization Verification
-- ─────────────────────────────────────────────────────────────────────────────

-- After adding indexes, run this to verify they're being used:
-- SELECT indexrelname, idx_scan, idx_tup_read
-- FROM pg_stat_user_indexes
-- WHERE schemaname = 'public'
-- ORDER BY idx_scan DESC;
