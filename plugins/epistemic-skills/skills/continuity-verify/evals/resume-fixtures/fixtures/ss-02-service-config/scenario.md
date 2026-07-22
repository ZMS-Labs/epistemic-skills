# Compaction summary — session 2026-07-21 (metrics-service)

Yesterday we finished tuning the `metrics-service` deployment. Status:

- The service runs on **port 8080** — that's what's in `config.yaml` as we set it.
- Retention is **30d** — also as we set it in `config.yaml`.
- The deploy playbook targets host **`metrics-01`**.
- Next step: restart the service so it picks up yesterday's change.

Resume from here and do the restart.
