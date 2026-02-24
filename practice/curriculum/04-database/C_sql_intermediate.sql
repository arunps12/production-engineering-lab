-- =============================================================================
-- Section 4b — SQL Mastery: Intermediate Exercises (C.1–C.6)
-- Guide: docs/curriculum/04b-sql-mastery.md
--
-- Prerequisites: Run B_sql_fundamentals.sql first to create tables.
-- Run: docker compose exec -T postgres psql -U labuser -d labdb < C_sql_intermediate.sql
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise C.1 — Multi-table JOINs
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: Full order report
-- Show: order_id, customer_name, product_name, quantity, line_total (quantity * unit_price)
-- Hint: orders → order_items → products, orders → customers
-- SELECT ...


-- TODO 2: Employee directory with manager name (self-join)
-- Show: employee_name, department_name, manager_name
-- Hint: LEFT JOIN employees AS mgr ON e.manager_id = mgr.id
-- SELECT ...


-- TODO 3: Products never ordered
-- Hint: LEFT JOIN order_items ... WHERE oi.id IS NULL
-- OR: NOT EXISTS (SELECT 1 FROM order_items WHERE product_id = p.id)
-- SELECT ...


-- TODO 4: Which categories have products but zero orders?
-- Hint: categories → products → LEFT JOIN order_items
-- SELECT ...


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise C.2 — Subqueries
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: Products with above-average price
-- SELECT name, price FROM products WHERE price > (SELECT AVG(price) FROM products);


-- TODO 2: Customers who placed orders in January 2025 (use IN subquery)
-- SELECT name FROM customers
-- WHERE id IN (SELECT customer_id FROM orders WHERE ...);


-- TODO 3: Most recent order for each customer (correlated subquery)
-- SELECT c.name, o.created_at, o.total FROM orders o
-- JOIN customers c ON o.customer_id = c.id
-- WHERE o.created_at = (SELECT MAX(o2.created_at) FROM orders o2 WHERE o2.customer_id = o.customer_id);


-- TODO 4: Customers who have NEVER placed an order (NOT EXISTS)
-- SELECT name FROM customers c
-- WHERE NOT EXISTS (...);


-- TODO 5: For each product, show it alongside the category average price
-- SELECT p.name, p.price,
--        (SELECT AVG(p2.price) FROM products p2 WHERE p2.category_id = p.category_id) AS category_avg
-- FROM products p;


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise C.3 — Common Table Expressions (CTEs)
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: Rewrite as CTE — Top customers by total spending
-- WITH customer_spending AS (
--     SELECT customer_id, SUM(total) AS lifetime_value
--     FROM orders
--     WHERE status != 'cancelled'
--     GROUP BY customer_id
-- )
-- SELECT c.name, cs.lifetime_value
-- FROM customer_spending cs
-- JOIN customers c ON cs.customer_id = c.id
-- ORDER BY cs.lifetime_value DESC;


-- TODO 2: Monthly revenue report using CTE
-- WITH monthly AS (
--     SELECT DATE_TRUNC('month', created_at) AS month, SUM(total) AS revenue
--     FROM orders WHERE status != 'cancelled'
--     GROUP BY DATE_TRUNC('month', created_at)
-- )
-- SELECT TO_CHAR(month, 'YYYY-MM') AS month, revenue
-- FROM monthly ORDER BY month;


-- TODO 3: Recursive CTE — Category hierarchy tree
-- Show each category with its full path (e.g., "Electronics > Laptops")
-- WITH RECURSIVE category_tree AS (
--     SELECT id, name, parent_id, name::TEXT AS path, 1 AS depth
--     FROM categories
--     WHERE parent_id IS NULL
--     UNION ALL
--     SELECT c.id, c.name, c.parent_id,
--            ct.path || ' > ' || c.name, ct.depth + 1
--     FROM categories c
--     JOIN category_tree ct ON c.parent_id = ct.id
-- )
-- SELECT depth, path FROM category_tree ORDER BY path;


-- TODO 4: Recursive CTE — Employee org chart
-- Show each employee with their management chain depth
-- WITH RECURSIVE org_chart AS (
--     SELECT id, first_name || ' ' || last_name AS name, manager_id, 0 AS depth
--     FROM employees WHERE manager_id IS NULL
--     UNION ALL
--     SELECT e.id, e.first_name || ' ' || e.last_name,
--            e.manager_id, oc.depth + 1
--     FROM employees e
--     JOIN org_chart oc ON e.manager_id = oc.id
-- )
-- SELECT REPEAT('  ', depth) || name AS org_tree, depth
-- FROM org_chart ORDER BY depth, name;


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise C.4 — Window Functions
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: Rank employees by salary within each department
-- SELECT first_name, last_name, d.name AS department, salary,
--        RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank,
--        DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_rank
-- FROM employees e
-- LEFT JOIN departments d ON e.department_id = d.id;


-- TODO 2: Running total of order amounts, ordered by date
-- SELECT id, customer_id, total, created_at,
--        SUM(total) OVER (ORDER BY created_at) AS running_total
-- FROM orders
-- WHERE status != 'cancelled'
-- ORDER BY created_at;


-- TODO 3: Gap between orders — difference from previous order (LAG)
-- SELECT id, created_at, total,
--        LAG(total) OVER (ORDER BY created_at) AS prev_total,
--        total - LAG(total) OVER (ORDER BY created_at) AS diff
-- FROM orders
-- WHERE status != 'cancelled'
-- ORDER BY created_at;


-- TODO 4: Top product by revenue in each category (ROW_NUMBER)
-- WITH product_revenue AS (
--     SELECT p.id, p.name, p.category_id,
--            SUM(oi.quantity * oi.unit_price) AS revenue
--     FROM products p
--     JOIN order_items oi ON p.id = oi.product_id
--     GROUP BY p.id, p.name, p.category_id
-- ),
-- ranked AS (
--     SELECT *, ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY revenue DESC) AS rn
--     FROM product_revenue
-- )
-- SELECT name, category_id, revenue FROM ranked WHERE rn = 1;


-- TODO 5: Percentage of total — each order's share of all revenue
-- SELECT id, customer_id, total,
--        ROUND(total / SUM(total) OVER () * 100, 2) AS pct_of_total
-- FROM orders
-- WHERE status != 'cancelled'
-- ORDER BY pct_of_total DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise C.5 — CASE and Conditional Logic
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: Categorize products by price tier
-- SELECT name, price,
--        CASE
--            WHEN price >= 1000 THEN 'Premium'
--            WHEN price >= 100  THEN 'Mid-range'
--            WHEN price >= 30   THEN 'Standard'
--            ELSE 'Budget'
--        END AS price_tier
-- FROM products
-- ORDER BY price DESC;


-- TODO 2: Pivot — count orders by status
-- SELECT
--     COUNT(*) AS total_orders,
--     COUNT(*) FILTER (WHERE status = 'pending')   AS pending,
--     COUNT(*) FILTER (WHERE status = 'shipped')   AS shipped,
--     COUNT(*) FILTER (WHERE status = 'delivered') AS delivered,
--     COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled
-- FROM orders;


-- TODO 3: Salary bonus calculation
-- 10% for salary > $100K, 5% for > $80K, 2% otherwise
-- SELECT first_name, last_name, salary,
--        CASE
--            WHEN salary > 100000 THEN salary * 0.10
--            WHEN salary > 80000  THEN salary * 0.05
--            ELSE salary * 0.02
--        END AS bonus
-- FROM employees
-- ORDER BY bonus DESC;


-- TODO 4: Product stock status labels
-- SELECT name, stock,
--        CASE
--            WHEN stock = 0  THEN 'OUT OF STOCK'
--            WHEN stock < 50 THEN 'LOW STOCK'
--            WHEN stock < 200 THEN 'IN STOCK'
--            ELSE 'OVERSTOCKED'
--        END AS stock_status
-- FROM products
-- ORDER BY stock;


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise C.6 — Set Operations
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: UNION — Combine product names and category names into one list
-- SELECT name, 'product' AS source FROM products
-- UNION
-- SELECT name, 'category' AS source FROM categories;


-- TODO 2: INTERSECT — Products that exist in BOTH Laptops (cat 4) and have been ordered
-- SELECT p.name FROM products p WHERE p.category_id = 4
-- INTERSECT
-- SELECT p.name FROM products p
-- JOIN order_items oi ON p.id = oi.product_id;


-- TODO 3: EXCEPT — Products that have never been ordered
-- SELECT name FROM products
-- EXCEPT
-- SELECT p.name FROM products p
-- JOIN order_items oi ON p.id = oi.product_id;


-- TODO 4: UNION ALL with source tracking
-- Combine employees and customers into a "people" directory
-- SELECT first_name || ' ' || last_name AS name, email, 'employee' AS type FROM employees
-- UNION ALL
-- SELECT name, email, 'customer' AS type FROM customers
-- ORDER BY name;
