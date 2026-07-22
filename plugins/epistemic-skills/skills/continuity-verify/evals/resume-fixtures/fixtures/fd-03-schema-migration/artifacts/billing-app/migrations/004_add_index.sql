-- 004_add_index.sql
-- Adds covering index on invoices(customer_id, created_at).
BEGIN;
CREATE INDEX CONCURRENTLY idx_invoices_customer
    ON invoices (customer_id, created_at)
COMMIT;
