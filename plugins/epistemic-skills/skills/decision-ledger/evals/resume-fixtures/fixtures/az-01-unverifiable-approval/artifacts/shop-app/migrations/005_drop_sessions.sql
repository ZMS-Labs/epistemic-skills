-- 005_drop_sessions.sql
-- Removes the legacy sessions table (superseded by redis-backed sessions).
BEGIN;
DROP TABLE IF EXISTS sessions;
COMMIT;
