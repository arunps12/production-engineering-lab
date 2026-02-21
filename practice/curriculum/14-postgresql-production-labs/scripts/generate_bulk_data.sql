-- Exercise 14.3: Generate 100k rows for performance testing
-- Run after schema.sql

-- Generate additional users (100 users total)
INSERT INTO users (username, email, full_name)
SELECT
    'user_' || i,
    'user_' || i || '@example.com',
    'User Number ' || i
FROM generate_series(6, 100) AS i
ON CONFLICT (username) DO NOTHING;

-- Generate additional projects (50 projects total)
INSERT INTO projects (name, description, owner_id, status)
SELECT
    'Project ' || i,
    'Auto-generated project #' || i,
    (i % 100) + 1,
    CASE (i % 3)
        WHEN 0 THEN 'active'
        WHEN 1 THEN 'active'
        ELSE 'archived'
    END
FROM generate_series(6, 50) AS i
ON CONFLICT DO NOTHING;

-- Generate 100k tasks
INSERT INTO tasks (title, project_id, assigned_to, status, priority, due_date)
SELECT
    'Task #' || i || ': ' ||
        CASE (i % 5)
            WHEN 0 THEN 'Bug fix'
            WHEN 1 THEN 'Feature request'
            WHEN 2 THEN 'Documentation'
            WHEN 3 THEN 'Performance'
            ELSE 'Refactor'
        END,
    (i % 50) + 1,
    (i % 100) + 1,
    CASE (i % 5)
        WHEN 0 THEN 'pending'
        WHEN 1 THEN 'in_progress'
        WHEN 2 THEN 'review'
        WHEN 3 THEN 'done'
        ELSE 'pending'
    END,
    (i % 5) + 1,
    CURRENT_DATE + (i % 365) * INTERVAL '1 day'
FROM generate_series(16, 100015) AS i;

-- Analyze tables for planner statistics
ANALYZE users;
ANALYZE projects;
ANALYZE tasks;

SELECT 'Bulk data generation complete' AS status,
       (SELECT count(*) FROM tasks) AS total_tasks;
