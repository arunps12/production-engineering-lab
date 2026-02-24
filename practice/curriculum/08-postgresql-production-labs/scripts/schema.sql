-- Exercise 14.2: Schema Design
-- Tables: users, projects, tasks, audit_logs

BEGIN;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(255) NOT NULL UNIQUE,
    full_name     VARCHAR(200) NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT true,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(200) NOT NULL,
    description   TEXT,
    owner_id      INTEGER      NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status        VARCHAR(20)  NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active', 'archived', 'paused')),
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id            SERIAL PRIMARY KEY,
    title         VARCHAR(300) NOT NULL,
    description   TEXT,
    project_id    INTEGER      NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    assigned_to   INTEGER      REFERENCES users(id) ON DELETE SET NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'in_progress', 'review', 'done', 'cancelled')),
    priority      INTEGER      NOT NULL DEFAULT 3
                  CHECK (priority BETWEEN 1 AND 5),
    due_date      DATE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id            BIGSERIAL PRIMARY KEY,
    entity_type   VARCHAR(50)  NOT NULL,
    entity_id     INTEGER      NOT NULL,
    action        VARCHAR(20)  NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values    JSONB,
    new_values    JSONB,
    performed_by  INTEGER      REFERENCES users(id) ON DELETE SET NULL,
    performed_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_email       ON users (email);
CREATE INDEX IF NOT EXISTS idx_tasks_project_id   ON tasks (project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to   ON tasks (assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_status_priority ON tasks (status, priority);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity   ON audit_logs (entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_performed_at ON audit_logs (performed_at);

COMMIT;

-- Verify
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' ORDER BY table_name;
