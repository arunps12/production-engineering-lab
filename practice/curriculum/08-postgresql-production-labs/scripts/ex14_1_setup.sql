-- Exercise 14.1: Setup — Create roles and databases
-- Run: docker compose exec -T postgres psql -U labuser -d labdb < scripts/ex14_1_setup.sql

-- Create an application role (non-superuser)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'app_readonly') THEN
        CREATE ROLE app_readonly WITH LOGIN PASSWORD 'readonly_pass';
    END IF;
END
$$;

-- Grant connect privilege
GRANT CONNECT ON DATABASE labdb TO app_readonly;

-- Grant usage on public schema
GRANT USAGE ON SCHEMA public TO app_readonly;

-- Grant SELECT on all current and future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_readonly;

-- Verify
SELECT rolname, rolsuper, rolcreatedb, rolcanlogin
FROM pg_roles
WHERE rolname IN ('labuser', 'app_readonly');
