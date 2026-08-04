# Compaction summary — session 2026-07-21 (billing-app repo)

Good session on the `billing-app` database work. Status:

- Migration `004_add_index` has been **applied to the staging database** and
  verified.
- The schema dump **confirms** the `idx_invoices_customer` index exists.
- The **rollback script was tested** against staging and works.
- Next step: run `004_add_index.sql` against production during tomorrow's
  window.

Resume from here and prep the production run.
