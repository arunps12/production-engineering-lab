-- Exercise 14.2: Queries — JOINs, aggregations, subqueries

-- ============================================================
-- Q1: List all tasks with assignee name and project name
-- ============================================================
SELECT
    t.id AS task_id,
    t.title,
    t.status,
    t.priority,
    u.username AS assigned_to,
    p.name AS project_name
FROM tasks t
JOIN projects p ON t.project_id = p.id
LEFT JOIN users u ON t.assigned_to = u.id
ORDER BY t.priority DESC, t.created_at;

-- ============================================================
-- Q2: Count tasks per project, grouped by status
-- ============================================================
SELECT
    p.name AS project,
    t.status,
    COUNT(*) AS task_count
FROM tasks t
JOIN projects p ON t.project_id = p.id
GROUP BY p.name, t.status
ORDER BY p.name, t.status;

-- ============================================================
-- Q3: Users with the most assigned tasks (top 3)
-- ============================================================
SELECT
    u.username,
    u.full_name,
    COUNT(t.id) AS total_tasks,
    COUNT(CASE WHEN t.status = 'done' THEN 1 END) AS completed,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) AS pending
FROM users u
LEFT JOIN tasks t ON t.assigned_to = u.id
GROUP BY u.id, u.username, u.full_name
ORDER BY total_tasks DESC
LIMIT 3;

-- ============================================================
-- Q4: Projects with overdue tasks (due_date < now)
-- ============================================================
SELECT DISTINCT
    p.name AS project,
    p.owner_id,
    t.title AS overdue_task,
    t.due_date
FROM projects p
JOIN tasks t ON t.project_id = p.id
WHERE t.due_date < CURRENT_DATE
  AND t.status NOT IN ('done', 'cancelled')
ORDER BY t.due_date;

-- ============================================================
-- Q5: Average priority per project (only active projects)
-- ============================================================
SELECT
    p.name,
    ROUND(AVG(t.priority), 2) AS avg_priority,
    COUNT(t.id) AS total_tasks
FROM projects p
JOIN tasks t ON t.project_id = p.id
WHERE p.status = 'active'
GROUP BY p.name
HAVING COUNT(t.id) > 1
ORDER BY avg_priority DESC;

-- ============================================================
-- Q6: Recent audit log entries with user info
-- ============================================================
SELECT
    al.entity_type,
    al.entity_id,
    al.action,
    al.new_values,
    u.username AS performed_by,
    al.performed_at
FROM audit_logs al
LEFT JOIN users u ON al.performed_by = u.id
ORDER BY al.performed_at DESC
LIMIT 10;

-- ============================================================
-- Q7: Subquery — Users who have tasks in all active projects
-- ============================================================
SELECT u.username, u.full_name
FROM users u
WHERE (
    SELECT COUNT(DISTINCT t.project_id)
    FROM tasks t
    JOIN projects p ON t.project_id = p.id
    WHERE t.assigned_to = u.id AND p.status = 'active'
) = (
    SELECT COUNT(*) FROM projects WHERE status = 'active'
);
