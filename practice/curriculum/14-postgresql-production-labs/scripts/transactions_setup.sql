-- Exercise 14.4: Transactions Lab Setup — Accounts table

BEGIN;

CREATE TABLE IF NOT EXISTS accounts (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    balance NUMERIC(12, 2) NOT NULL DEFAULT 0.00
            CHECK (balance >= 0)
);

-- Seed accounts
INSERT INTO accounts (name, balance) VALUES
    ('Alice Checking',  1000.00),
    ('Bob Checking',     500.00),
    ('Charlie Savings', 2500.00)
ON CONFLICT DO NOTHING;

COMMIT;

SELECT * FROM accounts;
