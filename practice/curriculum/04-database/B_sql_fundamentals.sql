-- =============================================================================
-- Section 4b — SQL Mastery: Beginner Exercises (B.1–B.6)
-- Guide: docs/curriculum/04b-sql-mastery.md
--
-- Run: docker compose exec -T postgres psql -U labuser -d labdb < B_sql_fundamentals.sql
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise B.1 — Setup: Create and Populate Practice Tables
-- ─────────────────────────────────────────────────────────────────────────────

-- Drop existing tables (safe for re-runs)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Departments
CREATE TABLE departments (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO departments (name) VALUES
    ('Engineering'), ('Marketing'), ('Sales'),
    ('Support'), ('HR'), ('Finance');

-- Employees (with self-referencing manager)
CREATE TABLE employees (
    id            SERIAL PRIMARY KEY,
    first_name    VARCHAR(50) NOT NULL,
    last_name     VARCHAR(50) NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    manager_id    INTEGER REFERENCES employees(id),
    salary        NUMERIC(10,2) NOT NULL,
    hire_date     DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO employees (first_name, last_name, email, department_id, manager_id, salary, hire_date) VALUES
    ('Alice',   'Chen',     'alice@company.com',    1, NULL, 130000, '2020-03-15'),
    ('Bob',     'Smith',    'bob@company.com',      1, 1,    110000, '2021-06-01'),
    ('Charlie', 'Davis',    'charlie@company.com',  1, 1,    105000, '2022-01-10'),
    ('Diana',   'Wilson',   'diana@company.com',    2, NULL, 95000,  '2020-07-22'),
    ('Eve',     'Johnson',  'eve@company.com',      2, 4,    85000,  '2023-02-14'),
    ('Frank',   'Brown',    'frank@company.com',    3, NULL, 90000,  '2019-11-30'),
    ('Grace',   'Lee',      'grace@company.com',    3, 6,    88000,  '2022-05-18'),
    ('Henry',   'Taylor',   'henry@company.com',    3, 6,    82000,  '2023-08-01'),
    ('Ivy',     'Martinez', 'ivy@company.com',      4, NULL, 75000,  '2021-09-12'),
    ('Jack',    'Anderson', 'jack@company.com',     4, 9,    70000,  '2024-01-05'),
    ('Karen',   'Thomas',   'karen@company.com',    5, NULL, 92000,  '2020-04-20'),
    ('Leo',     'Garcia',   'leo@company.com',      6, NULL, 115000, '2019-08-15'),
    ('Mia',     'Robinson', 'mia@company.com',      NULL, NULL, 65000, '2024-06-01');

-- Categories
CREATE TABLE categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    parent_id INTEGER REFERENCES categories(id)
);

INSERT INTO categories (name, parent_id) VALUES
    ('Electronics', NULL),       -- 1
    ('Books', NULL),             -- 2
    ('Clothing', NULL),          -- 3
    ('Laptops', 1),              -- 4
    ('Phones', 1),               -- 5
    ('Fiction', 2),              -- 6
    ('Non-Fiction', 2),          -- 7
    ('Men', 3),                  -- 8
    ('Women', 3);                -- 9

-- Products
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    description TEXT,
    price       NUMERIC(10,2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    stock       INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMP DEFAULT NOW()
);

INSERT INTO products (name, description, price, category_id, stock) VALUES
    ('MacBook Pro 14"',    'Apple laptop with M3 chip',       1999.99, 4, 50),
    ('ThinkPad X1 Carbon', 'Lenovo business ultrabook',       1499.99, 4, 35),
    ('iPhone 16',          'Latest Apple smartphone',          999.99, 5, 200),
    ('Pixel 9',            'Google flagship phone',            799.99, 5, 150),
    ('DDIA',               'Designing Data-Intensive Apps',     45.99, 7, 500),
    ('Clean Code',         'Robert C. Martin',                 35.99, 7, 300),
    ('Dune',               'Frank Herbert sci-fi classic',     12.99, 6, 400),
    ('Foundation',         'Isaac Asimov',                     14.99, 6, 350),
    ('Running Shoes',      NULL,                               89.99, 8, 100),
    ('Winter Jacket',      'Waterproof, insulated',           149.99, 8, 75),
    ('Summer Dress',       'Lightweight cotton',               59.99, 9, 120),
    ('Widget Pro',         'Professional-grade widget',         9.99, NULL, 1000);

-- Customers
CREATE TABLE customers (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(255) UNIQUE NOT NULL,
    city       VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO customers (name, email, city) VALUES
    ('Acme Corp',     'orders@acme.com',      'New York'),
    ('TechStart',     'buy@techstart.io',     'San Francisco'),
    ('DataFlow',      'purchasing@dataflow.ai','Austin'),
    ('CloudNine',     'ops@cloudnine.dev',    'Seattle'),
    ('ByteWorks',     'admin@byteworks.com',  'Boston'),
    ('NullPointer',   'info@nullptr.io',      'Portland'),
    ('InactiveInc',   'admin@inactive.com',   NULL);

-- Orders
CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status      VARCHAR(20) NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    total       NUMERIC(10,2),
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Order Items
CREATE TABLE order_items (
    id         SERIAL PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL
);

-- Insert orders spanning several months
INSERT INTO orders (customer_id, status, total, created_at) VALUES
    (1, 'delivered',  2045.98, '2025-01-15 10:30:00'),
    (1, 'delivered',   81.98,  '2025-02-20 14:00:00'),
    (2, 'delivered',  1999.99, '2025-01-22 09:15:00'),
    (2, 'shipped',     45.99,  '2025-03-10 11:45:00'),
    (3, 'delivered',   59.97,  '2025-02-05 16:20:00'),
    (3, 'shipped',    149.99,  '2025-03-15 08:30:00'),
    (4, 'pending',    799.99,  '2025-04-01 13:00:00'),
    (4, 'delivered',   89.99,  '2025-01-30 10:00:00'),
    (5, 'shipped',    1499.99, '2025-03-25 15:45:00'),
    (5, 'cancelled',   35.99,  '2025-02-28 12:00:00'),
    (6, 'pending',     27.98,  '2025-04-05 09:30:00');

-- Order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1,  1, 1999.99),  -- MacBook
    (1, 5,  1,   45.99),  -- DDIA
    (2, 5,  1,   45.99),  -- DDIA
    (2, 6,  1,   35.99),  -- Clean Code
    (3, 1,  1, 1999.99),  -- MacBook
    (4, 5,  1,   45.99),  -- DDIA
    (5, 7,  3,   12.99),  -- Dune x3
    (5, 8,  1,   14.99),  -- Foundation
    (6, 10, 1,  149.99),  -- Winter Jacket
    (7, 4,  1,  799.99),  -- Pixel 9
    (8, 9,  1,   89.99),  -- Running Shoes
    (9, 2,  1, 1499.99),  -- ThinkPad
    (10, 6, 1,   35.99),  -- Clean Code
    (11, 7, 1,   12.99),  -- Dune
    (11, 8, 1,   14.99);  -- Foundation


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise B.2 — Basic SELECT and Filtering
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: All employees in the Engineering department (department_id = 1)
-- SELECT ...

-- TODO 2: Products with price between $10 and $50
-- SELECT ...

-- TODO 3: Customers whose email contains "company" (use LIKE or ILIKE)
-- SELECT ...

-- TODO 4: Orders placed in Q1 2025 (Jan-Mar)
-- SELECT ...

-- TODO 5: Products that have no description (NULL)
-- SELECT ...


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise B.3 — Sorting and Pagination
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: All products sorted by price descending
-- SELECT ...

-- TODO 2: The 5 most recent orders
-- SELECT ...

-- TODO 3: Top 3 highest-paid employees
-- SELECT ...

-- TODO 4: Products page 2 (items 5-8) sorted by name alphabetically
-- Hint: LIMIT 4 OFFSET 4
-- SELECT ...


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise B.4 — Aggregate Functions
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: Total number of orders
-- SELECT COUNT(*) ...

-- TODO 2: Average order total
-- SELECT AVG(total) ...

-- TODO 3: Most expensive product (name and price)
-- SELECT ...

-- TODO 4: Earliest and latest order dates
-- SELECT MIN(...), MAX(...) ...

-- TODO 5: Number of distinct cities among customers
-- SELECT COUNT(DISTINCT ...) ...


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise B.5 — GROUP BY and HAVING
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: Number of employees per department (show department name)
-- Hint: JOIN departments then GROUP BY
-- SELECT ...

-- TODO 2: Total sales (SUM of total) per customer
-- SELECT ...

-- TODO 3: Average order total per order status
-- SELECT ...

-- TODO 4: Departments with more than 2 employees
-- Hint: HAVING COUNT(*) > 2
-- SELECT ...

-- TODO 5: Products ordered more than once (by count of order_items)
-- SELECT ...


-- ─────────────────────────────────────────────────────────────────────────────
-- Exercise B.6 — Simple JOINs
-- ─────────────────────────────────────────────────────────────────────────────

-- TODO 1: All orders with customer name (INNER JOIN)
-- SELECT c.name, o.id, o.total, o.status ...

-- TODO 2: All customers with their orders — include customers with no orders
-- Hint: LEFT JOIN
-- SELECT c.name, o.id, o.total ...

-- TODO 3: Order details with product name and price
-- Hint: orders → order_items → products
-- SELECT ...

-- TODO 4: Employees with their department name
-- Hint: LEFT JOIN departments (some employees have NULL department_id)
-- SELECT ...


-- ─────────────────────────────────────────────────────────────────────────────
-- VERIFICATION: Run after completing exercises to check your setup
-- ─────────────────────────────────────────────────────────────────────────────

SELECT '=== TABLE ROW COUNTS ===' AS info;
SELECT 'departments' AS tbl, COUNT(*) AS rows FROM departments
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'categories', COUNT(*) FROM categories
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
ORDER BY tbl;
