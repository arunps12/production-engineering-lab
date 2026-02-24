-- Exercise 14.2: Seed data
-- Run after schema.sql

BEGIN;

-- Users
INSERT INTO users (username, email, full_name) VALUES
    ('alice',   'alice@example.com',   'Alice Johnson'),
    ('bob',     'bob@example.com',     'Bob Smith'),
    ('charlie', 'charlie@example.com', 'Charlie Brown'),
    ('diana',   'diana@example.com',   'Diana Prince'),
    ('eve',     'eve@example.com',     'Eve Davis')
ON CONFLICT (username) DO NOTHING;

-- Projects
INSERT INTO projects (name, description, owner_id, status) VALUES
    ('Web Redesign',    'Redesign the company website',           1, 'active'),
    ('API Migration',   'Migrate REST API to v2',                 2, 'active'),
    ('Data Pipeline',   'Build ETL pipeline for analytics',       1, 'active'),
    ('Mobile App',      'Cross-platform mobile application',      3, 'paused'),
    ('DevOps Tooling',  'Internal CI/CD and monitoring tools',    4, 'active')
ON CONFLICT DO NOTHING;

-- Tasks
INSERT INTO tasks (title, project_id, assigned_to, status, priority, due_date) VALUES
    ('Design homepage mockup',        1, 1, 'done',        4, '2025-06-01'),
    ('Implement responsive layout',   1, 2, 'in_progress', 3, '2025-06-15'),
    ('Write API v2 spec',             2, 2, 'done',        5, '2025-05-20'),
    ('Implement /users endpoint',     2, 3, 'in_progress', 4, '2025-06-10'),
    ('Implement /projects endpoint',  2, 3, 'pending',     3, '2025-06-20'),
    ('Set up Airflow DAGs',           3, 4, 'pending',     5, '2025-07-01'),
    ('Create data quality checks',    3, 1, 'pending',     4, '2025-07-10'),
    ('Design app wireframes',         4, 5, 'review',      3, '2025-08-01'),
    ('Set up CI pipeline',            5, 4, 'done',        5, '2025-05-15'),
    ('Add monitoring dashboards',     5, 4, 'in_progress', 4, '2025-06-01'),
    ('Write unit tests for API v2',   2, 1, 'pending',     3, '2025-06-25'),
    ('Database migration plan',       2, 2, 'pending',     5, '2025-06-05'),
    ('Performance load testing',      5, 5, 'pending',     2, '2025-07-15'),
    ('Security audit',                5, 3, 'pending',     5, '2025-06-20'),
    ('User acceptance testing',       1, 5, 'pending',     3, '2025-07-01')
ON CONFLICT DO NOTHING;

-- Audit logs (sample entries)
INSERT INTO audit_logs (entity_type, entity_id, action, new_values, performed_by) VALUES
    ('project', 1, 'INSERT', '{"name": "Web Redesign", "status": "active"}'::jsonb, 1),
    ('task',    1, 'INSERT', '{"title": "Design homepage mockup", "status": "pending"}'::jsonb, 1),
    ('task',    1, 'UPDATE', '{"status": "done"}'::jsonb, 1),
    ('task',    3, 'UPDATE', '{"status": "done"}'::jsonb, 2),
    ('project', 4, 'UPDATE', '{"status": "paused"}'::jsonb, 3);

COMMIT;

SELECT 'Seed complete' AS status,
       (SELECT count(*) FROM users) AS users,
       (SELECT count(*) FROM projects) AS projects,
       (SELECT count(*) FROM tasks) AS tasks,
       (SELECT count(*) FROM audit_logs) AS audit_logs;
